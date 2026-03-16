# .py version of 02_plant_disease_query.ipynb
# Name: Zihan

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: Plant disease classification inference script.

# 1. Standard Library
import argparse
import json
import warnings
from pathlib import Path

# 2. Third-party Libraries
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

# ====================================================================
# 1. Global Settings and Helper Functions
# ====================================================================

# Ignore warnings that don't affect results
warnings.filterwarnings('ignore')

# Image transforms used for inference, must be exactly the same as validation/test transforms during training
inference_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_class_map(json_path: Path):
    """Load index -> ID mapping dictionary from JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            idx_to_label = json.load(f)
        # JSON loaded keys are strings by default, we need to convert them to integers to match PyTorch output
        idx_to_label = {int(k): v for k, v in idx_to_label.items()}
        print("✅ Translation dictionary loaded successfully.")
        return idx_to_label
    except Exception as e:
        print(f"🛑 Error loading mapping file '{json_path}': {e}")
        return None

def load_model(model_name: str, num_classes: int, model_path: Path, device: torch.device):
    """Load model architecture and trained weights"""
    try:
        model = timm.create_model(model_name, pretrained=False, num_classes=num_classes)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)
        model.eval() # Switch to evaluation mode, this is very important!
        print("✅ Model loaded successfully.")
        return model
    except Exception as e:
        print(f"🛑 Error loading model '{model_path}': {e}")
        return None

def predict_topk(model: nn.Module, image_path: Path, transforms: transforms.Compose, 
                 idx_to_label_map: dict, device: torch.device, k: int = 3):
    """Perform Top-K prediction on a single image, output only ID and probability"""
    try:
        image = Image.open(image_path).convert("RGB")
        image_tensor = transforms(image).unsqueeze(0).to(device)
    except Exception as e:
        print(f"🛑 Error processing image '{image_path}': {e}")
        return None

    with torch.no_grad():
        logits = model(image_tensor)

    probabilities = F.softmax(logits, dim=1)
    topk_probs, topk_indices = torch.topk(probabilities, k, dim=1)

    topk_probs = topk_probs.squeeze().cpu().numpy()
    topk_indices = topk_indices.squeeze().cpu().numpy()
    
    results = []
    for i in range(k):
        class_idx = topk_indices[i]
        class_id = idx_to_label_map[class_idx]
        prob = topk_probs[i]
        
        results.append({
            "predicted_id": int(class_id),
            "probability": float(prob) # Return float instead of string for easier subsequent processing
        })
        
    return results

# ====================================================================
# 2. Main Program
# ====================================================================

def main():
    # --- Set command line arguments ---
    ap = argparse.ArgumentParser(description="Plant disease recognition inference script")
    ap.add_argument("--image", type=str, required=True, help="Single image path to predict")
    ap.add_argument("--model-path", type=str, default="model.pth", help="Trained model file path (.pth)")
    ap.add_argument("--class-map", type=str, default="class_map.json", help="Class index to ID mapping file (.json)")
    ap.add_argument("--topk", type=int, default=3, help="Return top K results with highest probability")
    ap.add_argument("--json", action="store_true", help="If set, output results in JSON format")
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # --- Convert path strings to Path objects ---
    model_path = Path(args.model_path)
    class_map_path = Path(args.class_map)
    image_path = Path(args.image)

    # --- Execute workflow ---
    idx_to_label = load_class_map(class_map_path)
    if not idx_to_label:
        return

    model = load_model("swin_base_patch4_window7_224.ms_in1k", len(idx_to_label), model_path, device)
    if not model:
        return
        
    if not image_path.exists():
        print(f"🛑 Error: Input image '{image_path}' does not exist.")
        return

    results = predict_topk(model, image_path, inference_transforms, idx_to_label, device, k=args.topk)

    # --- Output results ---
    if not results:
        print("🛑 Prediction failed.")
        return

    if args.json:
        # Output in JSON format
        # ensure_ascii=False ensures non-ASCII characters like Chinese can be displayed correctly
        print(json.dumps(results, indent=4, ensure_ascii=False))
    else:
        # Output in human-readable format
        print("\n" + "="*30)
        print("--- Prediction Results ---")
        print(f"Image: {image_path.name}")
        print("="*30)
        for pred in results:
            print(f"Disease ID: {pred['predicted_id']:<5} | Probability: {pred['probability']:.2%}")

# ====================================================================
# 3. Program Entry Point
# ====================================================================

if __name__ == "__main__":
    main()

# ====================================================================
# 4. Usage Examples (Run in terminal)
# ====================================================================
#
# python 02_plant_disease_query.py --image test_images/011d0.jfif
#
# python 02_plant_disease_query.py --image test_images/011d0.jfif --topk 3 --json
#
# python 02_plant_disease_query.py --image test_images/Appels.jfif --topk 3 --json