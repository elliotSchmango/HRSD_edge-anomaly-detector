import cv2
import numpy as np
import onnxruntime as ort
import time
from pathlib import Path

#Config
MODEL_PATH = "models/autoencoder/autoencoder.onnx"
CAMERA_INDEX = 0
IMG_SIZE = 224
THRESHOLD = 0.01

#load ONNX model
session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

#Initalize camera
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("[Error] Camera not accessible")
    exit(1)

print("[Sentry] Starting anomaly detection loop...")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Resize + normalize
        img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1)) #swap axes
        img = np.expand_dims(img, axis=0)

        #inference
        recon = session.run([output_name], {input_name: img})[0]

        # MSE anomaly score
        score = np.mean((img - recon) ** 2)
        print(f"[Sentry] MSE score: {score:.6f}")

        if score > THRESHOLD:
            print("[ALERT] Anomaly Detected!")

        time.sleep(1)

except KeyboardInterrupt:
    print("[Sentry] Interrupted")

cap.release()
cv2.destroyAllWindows()