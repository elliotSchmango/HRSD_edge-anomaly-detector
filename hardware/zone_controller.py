from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
import time

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard servo frequency

# Define pan/tilt channels and pulse mappings
PAN_CHANNEL = 0
TILT_CHANNEL = 1

# Zone angles with overlap (you can fine-tune these)
ZONE_ANGLES = {
    1: (60, 120),   # (pan, tilt)
    2: (90, 120),
    3: (120, 120),
    4: (60, 90),
    5: (90, 90),
    6: (120, 90),
    7: (60, 60),
    8: (90, 60),
    9: (120, 60)
}

def angle_to_pwm(angle):
    """Convert angle (0–180) to PWM pulse (min=150, max=600)"""
    return int((angle / 180.0) * 450 + 150)

def move_to_zone(zone_id):
    """Move to the given zone ID (1–9)"""
    if zone_id not in ZONE_ANGLES:
        raise ValueError(f"Invalid zone: {zone_id}")
    pan_angle, tilt_angle = ZONE_ANGLES[zone_id]
    pca.channels[PAN_CHANNEL].duty_cycle = angle_to_pwm(pan_angle)
    pca.channels[TILT_CHANNEL].duty_cycle = angle_to_pwm(tilt_angle)
    print(f"[ZoneController] Moving to Zone {zone_id}: Pan={pan_angle}, Tilt={tilt_angle}")
    time.sleep(1.0)  # Delay to allow servo movement

def cleanup():
    """Stop all PWM signals (optional at exit)"""
    pca.channels[PAN_CHANNEL].duty_cycle = 0
    pca.channels[TILT_CHANNEL].duty_cycle = 0