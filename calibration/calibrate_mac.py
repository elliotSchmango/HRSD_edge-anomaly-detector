import os
import cv2
import time
import random

# Settings
NUM_ZONES = 9
FRAMES_PER_ZONE = 5
SAVE_PATH = "calibration/data"
CAMERA_INDEX = 0
SAMPLE_RATE = 6  # every 6 frames, choose one at random

# This version skips servo control entirely (for Mac/webcam testing)
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
        time.sleep(0.03)  # ~30fps input pacing

def run_calibration():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[Error] Cannot open camera.")
        return

    print("[Info] Starting fake zone calibration using Mac webcam...")
    for zone in range(NUM_ZONES):
        print(f"[Mock] Simulating zone {zone}")
        capture_frames_for_zone(cap, zone)

    cap.release()
    print("[Done] Calibration complete.")

def main():
    run_calibration()

if __name__ == "__main__":
    main()