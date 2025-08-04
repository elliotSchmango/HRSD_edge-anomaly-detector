import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Setup I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60 #60 hz polling rate for servos

# Convert angle (0–180) to 16-bit duty cycle for MG996R servos
def angle_to_duty(angle):
    min_duty = 150  # pulse for 0°s
    max_duty = 600  # pulse for 180°
    pulse = int(min_duty + (angle / 180.0) * (max_duty - min_duty))
    return pulse << 4  # convert to 16-bit

# Define 3x3 zone angles with overlap
zone_angles = {
    0: (45, 60),   # Top-left
    1: (90, 60),   # Top-center
    2: (135, 60),  # Top-right
    3: (45, 90),   # Mid-left
    4: (90, 90),   # Mid-center
    5: (135, 90),  # Mid-right
    6: (45, 120),  # Bottom-left
    7: (90, 120),  # Bottom-center
    8: (135, 120)  # Bottom-right
}

# Move camera to specific zone (pan: channel 0, tilt: channel 1)
def move_to_zone(zone_id, pan_channel=0, tilt_channel=1):
    pan_angle, tilt_angle = zone_angles[zone_id]
    pca.channels[pan_channel].duty_cycle = angle_to_duty(pan_angle)
    pca.channels[tilt_channel].duty_cycle = angle_to_duty(tilt_angle)
    print(f"[Servo] Moved to zone {zone_id} → pan: {pan_angle}°, tilt: {tilt_angle}°")
    time.sleep(0.5)  # wait for servo to stabilize