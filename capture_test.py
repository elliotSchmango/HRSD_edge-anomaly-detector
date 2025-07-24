import cv2
from datetime import datetime

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[Error] Cannot open camera")
    exit()

# Read one frame
ret, frame = cap.read()
if not ret:
    print("[Error] Failed to grab frame")
    cap.release()
    exit()

# Save frame to file
filename = f"test_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
cv2.imwrite(filename, frame)
print(f"[Saved] Photo saved as {filename}")

cap.release()