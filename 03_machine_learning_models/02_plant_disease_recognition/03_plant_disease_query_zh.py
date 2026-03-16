# 02_plant_disease_query.ipynb 的 .py 版本
# 作者：Zihan

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 描述：植物疾病分类推理脚本

# 1. 标准库
import argparse                                     # 命令行参数解析
import json                                         # JSON 处理
import warnings                                     # 警告处理
from pathlib import Path                            # 路径处理

# 2. 第三方库
import timm                                         # PyTorch Image Models
import torch                                        # PyTorch 框架
import torch.nn as nn                               # 神经网络模块
import torch.nn.functional as F                     # 函数式接口
from PIL import Image                               # 图像处理
from torchvision import transforms                  # 图像变换

# ====================================================================
# 1. 全局设置和辅助函数
# ====================================================================

warnings.filterwarnings('ignore')                   # 忽略不影响结果的警告

# 推理时使用的图像转换，必须与训练时的验证/测试集转换完全一致
inference_transforms = transforms.Compose([
    transforms.Resize((224, 224)),                                      # 调整尺寸
    transforms.ToTensor(),                                              # 转换为 Tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406],                    # 归一化（ImageNet 均值）
                         std=[0.229, 0.224, 0.225])                     # 归一化（ImageNet 标准差）
])


def load_class_map(json_path: Path):
    """
    从 JSON 文件加载 索引→ID 的映射字典
    
    参数:
        json_path: JSON 文件路径
    
    返回:
        映射字典 {int: int}，加载失败时返回 None
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            idx_to_label = json.load(f)
        # JSON 加载的 key 默认是字符串，需转为整数以匹配 PyTorch 输出
        idx_to_label = {int(k): v for k, v in idx_to_label.items()}
        print("✅ 翻译词典加载成功。")
        return idx_to_label
    except Exception as e:
        print(f"🛑 加载映射文件 '{json_path}' 时出错：{e}")
        return None


def load_model(model_name: str, num_classes: int, model_path: Path, device: torch.device):
    """
    加载模型架构并载入训练好的权重
    
    参数:
        model_name: 模型名称（timm 格式）
        num_classes: 输出类别数
        model_path: 模型权重文件路径
        device: 计算设备
    
    返回:
        加载好的模型，加载失败时返回 None
    """
    try:
        model = timm.create_model(model_name, pretrained=False, num_classes=num_classes)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)                                                # 移动到设备
        model.eval()                                                    # 切换到评估模式
        print("✅ 模型加载成功。")
        return model
    except Exception as e:
        print(f"🛑 加载模型 '{model_path}' 时出错：{e}")
        return None


def predict_topk(model: nn.Module, image_path: Path, transforms: transforms.Compose,
                 idx_to_label_map: dict, device: torch.device, k: int = 3):
    """
    对单张图片进行 Top-K 预测，只输出 ID 和概率
    
    参数:
        model: 加载好的模型
        image_path: 输入图像路径
        transforms: 图像预处理管道
        idx_to_label_map: 索引→ID 的映射字典
        device: 计算设备
        k: 返回结果数量（默认 3）
    
    返回:
        Top-K 预测结果列表 [{"predicted_id": int, "probability": float}, ...]
        出错时返回 None
    """
    try:
        image = Image.open(image_path).convert("RGB")                   # 打开图像并转为 RGB
        image_tensor = transforms(image).unsqueeze(0).to(device)        # 预处理并增加 batch 维度
    except Exception as e:
        print(f"🛑 处理图像 '{image_path}' 时出错：{e}")
        return None

    with torch.no_grad():                                               # 关闭梯度计算
        logits = model(image_tensor)                                    # 前向传播

    probabilities = F.softmax(logits, dim=1)                            # 转换为概率
    topk_probs, topk_indices = torch.topk(probabilities, k, dim=1)      # 获取 Top-K

    topk_probs   = topk_probs.squeeze().cpu().numpy()                   # 移动到 CPU 并转为 NumPy
    topk_indices = topk_indices.squeeze().cpu().numpy()
    
    results = []
    for i in range(k):
        class_idx = topk_indices[i]
        class_id  = idx_to_label_map[class_idx]                         # 索引→ID 翻译
        prob      = topk_probs[i]
        
        results.append({
            "predicted_id": int(class_id),                              # 确保 ID 是整数
            "probability": float(prob)                                  # 返回 float 便于后续处理
        })
        
    return results


# ====================================================================
# 2. 主程序
# ====================================================================

def main():
    # --- 设置命令行参数 ---
    ap = argparse.ArgumentParser(description="植物疾病识别推理脚本")
    ap.add_argument("--image", type=str, required=True, help="待预测的单张图像路径")
    ap.add_argument("--model-path", type=str, default="model.pth", help="训练好的模型文件路径 (.pth)")
    ap.add_argument("--class-map", type=str, default="class_map.json", help="类别索引到 ID 的映射文件 (.json)")
    ap.add_argument("--topk", type=int, default=3, help="返回概率最高的 Top-K 个结果")
    ap.add_argument("--json", action="store_true", help="如果设置，以 JSON 格式输出结果")
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 检测设备
    print(f"使用设备：{device}")

    # --- 将路径字符串转换为 Path 对象 ---
    model_path     = Path(args.model_path)
    class_map_path = Path(args.class_map)
    image_path     = Path(args.image)

    # --- 执行工作流 ---
    idx_to_label = load_class_map(class_map_path)                     # 加载映射字典
    if not idx_to_label:
        return

    model = load_model("swin_base_patch4_window7_224.ms_in1k", len(idx_to_label),
                       model_path, device)                              # 加载模型
    if not model:
        return
        
    if not image_path.exists():                                       # 检查图像是否存在
        print(f"🛑 错误：输入图像 '{image_path}' 不存在。")
        return

    results = predict_topk(model, image_path, inference_transforms,
                           idx_to_label, device, k=args.topk)          # 执行预测

    # --- 输出结果 ---
    if not results:
        print("🛑 预测失败。")
        return

    if args.json:
        # 以 JSON 格式输出
        # ensure_ascii=False 确保中文等非 ASCII 字符能正确显示
        print(json.dumps(results, indent=4, ensure_ascii=False))
    else:
        # 以人类可读格式输出
        print("\n" + "="*30)
        print("--- 预测结果 ---")
        print(f"图像：{image_path.name}")
        print("="*30)
        for pred in results:
            print(f"病害 ID: {pred['predicted_id']:<5} | 概率：{pred['probability']:.2%}")


# ====================================================================
# 3. 程序入口
# ====================================================================

if __name__ == "__main__":
    main()


# ====================================================================
# 4. 使用示例（在终端运行）
# ====================================================================
#
# python 02_plant_disease_query.py --image test_images/011d0.jfif
#
# python 02_plant_disease_query.py --image test_images/011d0.jfif --topk 3 --json
#
# python 02_plant_disease_query.py --image test_images/Appels.jfif --topk 3 --json


# # 人类可读格式输出
# python 02_plant_disease_query.py --image test_images/xxx.jfif

# # JSON 格式输出（便于程序调用）
# python 02_plant_disease_query.py --image test_images/xxx.jfif --topk 3 --json

# # 自定义模型和映射文件路径
# python 02_plant_disease_query.py --image test_images/xxx.jfif \
#     --model-path /path/to/model.pth \
#     --class-map /path/to/class_map.json \
#     --topk 5 --json