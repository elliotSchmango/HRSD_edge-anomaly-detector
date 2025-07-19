import os
import cv2
import time
import random
from adafruit_servokit import ServoKit

#settings
NUM_ZONES = 9
FRAMES_PER_ZONE = 30
SAVE_PATH = "calibration/data"
CAMERA_INDEX = 0
SAMPLE_RATE = 6  # every 6 frames, choose one at random

#Servo config for SunFounder Pan/Tilt using PCA9685
kit = ServoKit(channels=16)
PAN_CHANNEL = 0
TILT_CHANNEL = 1

#Pan/tilt angles for 3x3 zone grid
# Angles should be tuned for your specific rig
ZONE_ANGLES = [
    (60, 60), (90, 60), (120, 60),
    (60, 90), (90, 90), (120, 90),
    (60, 120), (90, 120), (120, 120)
]

def move_to_zone(zone_index):
    if zone_index < 0 or zone_index >= len(ZONE_ANGLES):
        print(f"[Error] Invalid zone index: {zone_index}")
        return
    pan, tilt = ZONE_ANGLES[zone_index]
    print(f"[Servo] Moving to zone {zone_index} → pan={pan}, tilt={tilt}")
    kit.servo[PAN_CHANNEL].angle = pan
    kit.servo[TILT_CHANNEL].angle = tilt
    time.sleep(1.2)  #Buffered time for movement to complete

def capture_frames_for_zone(cap, zone_index):
    zone_dir = os.path.join(SAVE_PATH, f"zone_{zone_index}")
    os.makedirs(zone_dir, exist_ok=True)

    total_frames = FRAMES_PER_ZONE * SAMPLE_RATE
    selected_indices = sorted(random.sample(range(total_frames), FRAMES_PER_ZONE))

    frame_id = 0
    saved = 0
    while saved < FRAMES_PER_ZONE:
        ret, frame = cap.read()
        if not ret:
            print(f"[Error] Failed to capture frame {frame_id} in zone {zone_index}")
            continue

        if frame_id in selected_indices:
            filename = os.path.join(zone_dir, f"frame_{saved:03d}.png")
            cv2.imwrite(filename, frame)  # save full resolution
            print(f"Saved {filename}")
            saved += 1

        frame_id += 1
        time.sleep(0.03)  # ~30fps input, this approximates natural capture rate

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[Error] Cannot open camera.")
        return

    print("[Info] Starting calibration frame capture...")
    for zone in range(NUM_ZONES):
        move_to_zone(zone)
        capture_frames_for_zone(cap, zone)

    cap.release()
    print("[Done] Calibration complete.")

if __name__ == "__main__":
    main()