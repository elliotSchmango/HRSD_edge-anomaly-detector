import cv2

cap = cv2.VideoCapture(0)
ret, raw = cap.read()
cap.release()

if not ret:
    print("❌ Failed to capture frame.")
    exit(1)

# Convert YUYV to BGR
try:
    bgr = cv2.cvtColor(raw, cv2.COLOR_YUV2BGR_YUY2)
    cv2.imwrite("converted_yuyv.jpg", bgr)
    print("✅ Saved converted_yuyv.jpg (color-corrected)")
except Exception as e:
    print(f"❌ Failed to convert YUYV: {e}")