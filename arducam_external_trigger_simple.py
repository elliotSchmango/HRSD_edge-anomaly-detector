import os
import subprocess
import time
import cv2

def configure_camera_for_trigger():
    """
    Use v4l2-ctl to write Arducam IMX477 registers to enable external trigger mode.
    You must have the register map or reference script from Arducam.
    """
    print("[Config] Applying register settings for external trigger...")

    # Example: use Arducam's trigger_register.py or write registers manually
    # Replace with your known working config if needed
    subprocess.run([
        "v4l2-ctl", "-d", "/dev/video0",
        "--set-ctrl", "trigger_mode=1"
    ], check=False)

    # You may also need to write raw registers if trigger_mode control is missing
    # subprocess.run(["i2cset", "-y", "2", "0x1a", "0x0B", "0x01"], check=True)  # example

    print("[Config] Waiting for external trigger...")
    time.sleep(1)

def wait_for_trigger_and_capture():
    """
    Poll the video device for a triggered frame and save the result.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Error] Could not open /dev/video0")
        return

    print("[Trigger] Waiting for rising edge...")
    ret, frame = cap.read()

    if ret:
        filename = "trigger_capture.jpg"
        cv2.imwrite(filename, frame)
        print(f"[Success] Saved image: {filename}")
    else:
        print("[Error] Failed to capture frame")

    cap.release()

if __name__ == "__main__":
    configure_camera_for_trigger()
    wait_for_trigger_and_capture()