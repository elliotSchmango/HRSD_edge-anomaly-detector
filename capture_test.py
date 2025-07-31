import cv2

# Try default camera index (0); change to 1 or 2 if needed
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[Error] Could not open camera.")
    exit(1)

ret, frame = cap.read()
if not ret:
    print("[Error] Failed to grab frame.")
    exit(1)

cv2.imwrite("test_image.jpg", frame)
print("[Success] Saved test_image.jpg")

cap.release()