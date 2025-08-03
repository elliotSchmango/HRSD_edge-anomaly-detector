# utils.py

import torch
from PIL import Image
import torchvision.transforms as transforms

IMG_SIZE = 320
CLASS_NAMES = ["leak", "corrosion", "fire", "human"]

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)  # Add batch dimension

def softmax(logits):
    exp = torch.exp(logits - torch.max(logits))
    return exp / exp.sum(dim=1, keepdim=True)

def interpret_output(logits, threshold=0.85):
    probs = softmax(logits)
    conf, pred = torch.max(probs, dim=1)
    if conf.item() < threshold:
        return "unknown/other", conf.item()
    return CLASS_NAMES[pred.item()], conf.item()