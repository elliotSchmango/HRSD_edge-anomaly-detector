import cv2
import numpy as np
import onnxruntime as ort
import csv
import time
import os
from datetime import datetime

# === Model and Camera Config ===
MODEL_PATH = "models/autoencoder/autoencoder.onnx"
CAMERA_INDEX = 0
IMG_SIZE = 224
THRESHOLD = 0.01
ZONE_GRID_SIZE = 3  # 3x3 grid

# === Zone Angle Map (example; replace with your own angles) ===
zone_angles = {
    0: (30, 30),
    1: (90, 30),
    2: (150, 30),
    3: (150, 90),
    4: (90, 90),
    5: (30, 90),
    6: (30, 150),
    7: (90, 150),
    8: (150, 150)
}

# === Servo Control ===
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

def move_to_zone(zone_id):
    pan, tilt = zone_angles[zone_id]
    kit.servo[0].angle = pan
    kit.servo[1].angle = tilt
    print(f"[Move] Zone {zone_id} → Pan {pan}°, Tilt {tilt}°")
    time.sleep(0.5)

# === Snake-Pattern Zone Traversal ===
def get_snake_order(grid_size=3):
    grid = [[row * grid_size + col for col in range(grid_size)] for row in range(grid_size)]
    order = []
    for i, row in enumerate(grid):
        order.extend(row if i % 2 == 0 else reversed(row))
    return order

snake_order = get_snake_order(ZONE_GRID_SIZE)

# === Load ONNX Model ===
session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("[Error] Camera not accessible")
    exit(1)

print("[Sentry] Continuous snake-pattern monitoring...")

try:
    while True:
        if os.path.exists("sentry_stop.txt"):
            print("[Sentry] Stop signal received. Exiting.")
            break

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_path = f"sentry_results/sentry_results_{timestamp}.csv"
        with open(csv_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["zone", "mse", "anomaly"])

            for zone in snake_order:
                move_to_zone(zone)

                # Update GUI status file
                with open("status_zone.txt", "w") as sf:
                    sf.write(f"Scanning Zone {zone}")

                ret, frame = cap.read()
                if not ret:
                    print(f"[Warning] Frame grab failed for zone {zone}")
                    continue

                img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE)).astype(np.float32) / 255.0
                img = np.transpose(img, (2, 0, 1))
                img = np.expand_dims(img, axis=0)

                output = session.run([output_name], {input_name: img})[0]
                mse = np.mean((img - output) ** 2)
                is_anomaly = int(mse > THRESHOLD)

                print(f"[Zone {zone}] MSE: {mse:.5f} → {'ANOMALY' if is_anomaly else 'Normal'}")
                writer.writerow([zone, round(mse, 5), is_anomaly])

except KeyboardInterrupt:
    print("[Sentry] Interrupted by keyboard.")

# === Cleanup ===
cap.release()
if os.path.exists("sentry_stop.txt"):
    os.remove("sentry_stop.txt")
with open("status_zone.txt", "w") as sf:
    sf.write("Sentry Mode Off")

print("[Sentry] Finished. Camera released.")