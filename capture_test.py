gst = ("v4l2src device=/dev/video0 ! "
       "image/jpeg,width=1920,height=1080,framerate=30/1 ! "
       "jpegdec ! videoconvert ! appsink")

cap = cv2.VideoCapture(gst, cv2.CAP_GSTREAMER)
ret, frame = cap.read()
if ret:
    cv2.imwrite("gstreamer_capture.jpg", frame)
else:
    print("❌ GStreamer pipeline failed")