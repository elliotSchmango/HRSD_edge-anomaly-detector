import cv2
import subprocess

cap = cv2.VideoCapture(0)

#Force autofocus
subprocess.run(["v4l2-ctl", "-d", "/dev/video0", "--set-ctrl=focus_auto=1"])

#camera resolution should fall back
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

ret, frame = cap.read()
cap.release()

if not ret:
    print("Failed to capture frame")
else:
    print(f"Captured at resolution: {frame.shape[1]}x{frame.shape[0]}")
    cv2.imwrite("usb_maxres.jpg", frame)