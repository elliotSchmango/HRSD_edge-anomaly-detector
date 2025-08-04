import cv2
import os
import time
from hardware.zone_controller import move_to_zone

SAVE_PATH = "calibration/data"
FRAMES_PER_ZONE = 10

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("[Error] Camera not accessible")
    exit(1)

for zone_id in range(9):
    print(f"[Calibrate] Moving to zone {zone_id}")
    move_to_zone(zone_id)
    zone_dir = os.path.join(SAVE_PATH, f"zone_{zone_id}")
    os.makedirs(zone_dir, exist_ok=True)

    time.sleep(1.0)
    for i in range(FRAMES_PER_ZONE):
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(zone_dir, f"img_{i:03}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[Saved] {filename}")
        else:
            print(f"[Warning] Failed capture at zone {zone_id}, frame {i}")
        time.sleep(0.5)

print("[Calibrate] Done.")
cap.release()