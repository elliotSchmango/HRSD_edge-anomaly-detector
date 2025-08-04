import cv2

cap = cv2.VideoCapture(0)

#camera resolution should fall back
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 9999)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 9999)

ret, frame = cap.read()
cap.release()

if not ret:
    print("Failed to capture frame")
else:
    print(f"Captured at resolution: {frame.shape[1]}x{frame.shape[0]}")
    cv2.imwrite("usb_maxres.jpg", frame)