import cv2
from datetime import datetime

# GStreamer pipeline for Jetson CSI camera
pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! "
    "nvvidconv ! "
    "video/x-raw, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! appsink"
)

# Open camera using GStreamer pipeline
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("[Error] Cannot open CSI camera with GStreamer pipeline")
    exit()

# Read one frame
ret, frame = cap.read()
if not ret:
    print("[Error] Failed to grab frame")
    cap.release()
    exit()

#Save the frame to file
filename = f"csi_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
cv2.imwrite(filename, frame)
print(f"[Saved] Photo saved as {filename}")

cap.release()