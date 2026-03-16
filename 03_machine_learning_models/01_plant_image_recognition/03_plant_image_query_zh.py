# 02_plant_image_query.ipynb 的 .py 版本
# 作者：Zihan Yin

# 说明：本脚本使用 CLIP 模型实现植物图像相似度检索
#       通过测试时增强（TTA）提高查询鲁棒性
#       脚本加载预计算的嵌入向量，查找最相似的植物图像

# 核心组件：
# - EXIF 修正：确保图像方向正确
# - TTA 管道：包含几何变换和颜色变换
# - CLIP 模型：用于图像特征提取
# - 嵌入空间余弦相似度搜索
# - 支持表格和 JSON 两种输出格式

# 使用方法：python plant_image_query.py --image <路径> --k <top_k> --json

#!/usr/bin/env python3
import argparse, json                               # 命令行参数解析、JSON 处理
from pathlib import Path                            # 路径处理
import numpy as np                                  # 数值计算
from PIL import Image, ImageOps                     # 图像处理

import torch                                        # PyTorch 框架
from torch import nn                                # 神经网络模块
from torchvision import transforms                  # 图像变换/增强
from transformers import CLIPModel, CLIPProcessor   # CLIP 模型和处理器


# ============ 辅助函数 ============

def exif_correct(img: Image.Image) -> Image.Image:
    """修正图像方向并转换为 RGB 格式"""
    img = ImageOps.exif_transpose(img)              # 根据 EXIF 自动旋转
    if img.mode == "RGBA":                          # 处理透明通道
        bg = Image.new("RGB", img.size, (255, 255, 255))  # 白色背景
        bg.paste(img, mask=img.split()[-1])         # 使用 alpha 通道作为掩码
        return bg
    if img.mode != "RGB":                           # 确保为 RGB 格式
        img = img.convert("RGB")
    return img


def tta_pipeline():
    """轻量级测试时增强（TTA）管道"""
    return transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),                          # 随机水平翻转
        transforms.RandomAffine(degrees=10, translate=(0.06, 0.06),      # 小幅仿射变换
                                scale=(0.95, 1.05)),
        transforms.ColorJitter(brightness=0.1, contrast=0.1,             # 轻微颜色抖动
                               saturation=0.1, hue=0.01),
    ])


@torch.no_grad()  # 禁用梯度计算，节省内存
def encode_query(img: Image.Image, model, processor, device, tta_num=8):
    """
    对用户上传图像进行 TTA 增强编码，返回单个查询向量
    
    参数:
        img: PIL 图像对象
        model: CLIP 模型
        processor: CLIP 图像处理器
        device: 计算设备（cuda/cpu）
        tta_num: TTA 增强样本数量（默认 8，包含原图）
    
    返回:
        归一化的查询嵌入向量 (D,)
    """
    img = exif_correct(img)                              # EXIF 修正
    tta = tta_pipeline()                                 # 初始化 TTA 管道
    pil_list = [img] + [tta(img) for _ in range(max(tta_num-1, 0))]  # 原始图 + 增强图

    # 使用 CLIP 处理器预处理
    inputs = processor(images=pil_list, return_tensors="pt",
                       do_center_crop=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}  # 移动到设备

    # 混合精度推理（GPU 加速）
    with torch.autocast(device_type=("cuda" if device=="cuda" else "cpu"),
                        dtype=torch.float16, enabled=(device=="cuda")):
        feats = model.get_image_features(**inputs)         # 获取图像特征

    feats = nn.functional.normalize(feats, p=2, dim=-1)    # L2 归一化
    q = feats.mean(dim=0, keepdim=False)                   # 计算平均向量 (D,)
    return q.cpu().numpy().astype(np.float32)              # 转换为 NumPy 数组


def topk_cosine(query_emb, db_emb, plant_ids, k=10):
    """
    计算余弦相似度并返回 Top-K 匹配结果
    
    参数:
        query_emb: 查询向量 (D,)
        db_emb: 数据库嵌入矩阵 (N, D)，已 L2 归一化
        plant_ids: 植物 ID 数组
        k: 返回结果数量（默认 10）
    
    返回:
        Top-K 结果列表 [(plant_id, score), ...]
    """
    sims = db_emb @ query_emb                              # 余弦相似度（点积）
    idx = np.argpartition(-sims, kth=min(k, len(sims)-1))[:k]  # 高效获取 Top-K 索引
    idx = idx[np.argsort(-sims[idx])]                      # 按相似度降序排序
    return [(int(plant_ids[i]), float(sims[i])) for i in idx]  # 返回 (植物 ID, 分数)


# ============ 主程序 ============

def main():
    # 命令行参数解析
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", type=str, required=True, help="查询图像路径 (.jpg/.jpeg/.png)")
    ap.add_argument("--index", type=str, default="index/embeddings_fp16.npz", help="索引文件（建库时生成）")
    ap.add_argument("--meta", type=str, default="index/meta.json", help="元数据文件（建库时生成）")
    ap.add_argument("--model-local", type=str, default="clip-vit-b32", help="本地 CLIP 模型目录")
    ap.add_argument("--fallback-model-id", type=str, default="openai/clip-vit-base-patch32", help="本地失败时的在线模型 ID")
    ap.add_argument("--tta", type=int, default=8, help="TTA 迭代次数（包含原图）")
    ap.add_argument("--k", type=int, default=10, help="返回 Top-K 结果数量")
    ap.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    args = ap.parse_args()

    # 加载索引文件
    npz = np.load(args.index)
    db_emb    = npz["embeddings"].astype(np.float32)  # 数据库嵌入向量 (N, D)
    plant_ids = npz["plant_ids"]                      # 植物 ID 数组

    # 加载 CLIP 模型（优先在线下载，失败则加载本地）
    device = "cuda" if torch.cuda.is_available() else "cpu"  # 检测设备
    try:    
        print("正在尝试在线下载模型")
        model     = CLIPModel.from_pretrained(args.fallback_model_id)      # 从 Hugging Face 下载
        processor = CLIPProcessor.from_pretrained(args.fallback_model_id)
    except Exception:
        print("在线下载失败，尝试加载本地模型")
        model     = CLIPModel.from_pretrained(args.model_local)            # 从本地加载
        processor = CLIPProcessor.from_pretrained(args.model_local)

    model.eval().to(device)                                    # 设置评估模式并移动到设备

    # 读取并编码查询图像
    img = Image.open(args.image)                               # 打开查询图像
    q_emb = encode_query(img, model, processor, device, tta_num=args.tta)  # 编码查询向量

    # 执行相似度搜索
    results = topk_cosine(q_emb, db_emb, plant_ids, k=args.k)  # 获取 Top-K 结果

    # 输出结果
    if args.json:                                              # JSON 格式输出
        print(json.dumps([{"plant_id": pid, "score": score} for pid, score in results],
                         ensure_ascii=False, indent=2))
    else:                                                      # 表格格式输出
        for pid, score in results:
            print(f"{pid}\t{score:.4f}")


if __name__ == "__main__":
    main()


# ============ 测试命令示例 ============
# python 03_plant_image_query.py --image test_images/wechat_image_20250903174840_68_7.jpg --k 10 --tta 8 --json
# python 03_plant_image_query.py --image test_images/fdghjmhgferghthjkhgf.jpg --k 10 --tta 8 --json

# # 表格格式输出
# python plant_image_query.py --image test_images/xxx.jpg --k 10

# # JSON 格式输出（便于程序调用）
# python plant_image_query.py --image test_images/xxx.jpg --k 10 --json