import cv2
import os
import time
import numpy as np
import onnxruntime as ort
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from hardware.zone_controller import move_to_zone

# Config
IMG_SIZE = 224
THRESHOLD = 0.01
RESULTS_PATH = "sentry_results/sentry_log.csv"
STATUS_FILE = "status_zone.txt"
MODEL_PATH = "models/autoencoder/autoencoder.onnx"
CLASSIFIER_PATH = "models/classifier/classifier.onnx"

# Load models
ae_session = ort.InferenceSession(MODEL_PATH)
ae_input = ae_session.get_inputs()[0].name
ae_output = ae_session.get_outputs()[0].name

clf_session = ort.InferenceSession(CLASSIFIER_PATH)
clf_input = clf_session.get_inputs()[0].name
clf_output = clf_session.get_outputs()[0].name
CLASS_NAMES = ["Leak", "Corrosion", "Frayed Belt", "Human", "Foreign Object", "Lighting", "Fire", "Unknown"]

# Init camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("[Error] Camera not accessible")
    exit(1)

# Logging setup
os.makedirs("sentry_results", exist_ok=True)
if not os.path.exists(RESULTS_PATH):
    with open(RESULTS_PATH, "w") as f:
        f.write("timestamp,zone,mse,anomaly,label\n")

def run_autoencoder(frame):
    img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    out = ae_session.run([ae_output], {ae_input: img})[0]
    mse = np.mean((img - out) ** 2)
    return mse

def run_classifier(frame):
    img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    out = clf_session.run([clf_output], {clf_input: img})[0]
    pred_idx = np.argmax(out)
    return CLASS_NAMES[pred_idx]

print("[Sentry] Starting persistent scan loop...")

try:
    while True:
        for zone_id in range(9):
            move_to_zone(zone_id)
            time.sleep(0.5)

            ret, frame = cap.read()
            if not ret:
                print(f"[Warning] Failed to capture frame at zone {zone_id}")
                continue

            mse = run_autoencoder(frame)
            anomaly = mse > THRESHOLD
            label = run_classifier(frame) if anomaly else "Normal"

            with open(RESULTS_PATH, "a") as f:
                f.write(f"{datetime.now()},{zone_id},{mse:.5f},{anomaly},{label}\n")

            with open(STATUS_FILE, "w") as f:
                status_text = f"Zone {zone_id}: {label} ({'Anomaly' if anomaly else 'OK'})"
                f.write(status_text)

except KeyboardInterrupt:
    print("[Sentry] Terminated by user.")
    cap.release()