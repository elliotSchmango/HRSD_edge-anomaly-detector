from pathlib import Path
from PIL import Image
import torch
import torchvision.transforms as T
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import onnxruntime
import matplotlib.pyplot as plt

# Config
IMG_SIZE = 320
CLASS_NAMES = ["Corrosion", "Fire", "Human", "Leaky Pipes"]
TEST_DIR = Path("classifier_data/test_realworld")
MODEL_PATH = "models/classifier/classifier.onnx"

# Load model
session = onnxruntime.InferenceSession(MODEL_PATH)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Image preprocessing
transform = T.Compose([
    T.Resize((IMG_SIZE, IMG_SIZE)),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])
])

# Evaluation loop
y_true, y_pred = [], []

for folder in sorted(TEST_DIR.iterdir()):
    true_class = CLASS_NAMES.index(folder.name)
    for img_path in folder.glob("*.*"):
        img = Image.open(img_path).convert("RGB")
        x = transform(img).unsqueeze(0).numpy()
        output = session.run([output_name], {input_name: x})
        pred = torch.tensor(output[0]).argmax(dim=1).item()

        y_true.append(true_class)
        y_pred.append(pred)

# Metrics
print("\n📊 Classification Report:")
print(classification_report(y_true, y_pred, target_names=CLASS_NAMES, zero_division=0))

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
disp.plot(cmap="Blues")
plt.title("Real-World Test Set Confusion Matrix")
plt.show()