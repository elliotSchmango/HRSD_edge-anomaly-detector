import cv2
import os

# Optional: set a fixed output resolution
WIDTH, HEIGHT = 1920, 1080

# Capture raw Bayer image
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

if not cap.isOpened():
    print("[Error] Cannot open camera.")
    exit(1)

ret, raw = cap.read()
cap.release()

if not ret:
    print("[Error] Failed to capture image.")
    exit(1)

# Save raw frame
cv2.imwrite("raw_bayer.jpg", raw)

# Try all Bayer -> BGR modes
methods = {
    "BG": cv2.COLOR_BAYER_BG2BGR,
    "RG": cv2.COLOR_BAYER_RG2BGR,
    "GR": cv2.COLOR_BAYER_GR2BGR,
    "GB": cv2.COLOR_BAYER_GB2BGR
}

os.makedirs("demosaic_outputs", exist_ok=True)

for key, code in methods.items():
    try:
        bgr = cv2.cvtColor(raw, code)
        path = f"demosaic_outputs/demosaic_{key}.jpg"
        cv2.imwrite(path, bgr)
        print(f"[Saved] {path}")
    except Exception as e:
        print(f"[Error] {key} failed: {e}")