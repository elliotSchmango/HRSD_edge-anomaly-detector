import smbus2
import time

I2C_BUS = 1            # Jetson Orin Nano I2C bus
PCA_ADDRESS = 0x40     # Default I2C address of PCA9685

PAN_CHANNEL = 0
TILT_CHANNEL = 1

# Zones (pan, tilt) in degrees
ZONE_ANGLES = {
    1: (60, 120), 2: (90, 120), 3: (120, 120),
    4: (60, 90),  5: (90, 90),  6: (120, 90),
    7: (60, 60),  8: (90, 60),  9: (120, 60)
}

def angle_to_pwm(angle):
    """Convert angle to pulse length between 150 and 600."""
    return int((angle / 180.0) * 450 + 150)

def set_pwm(bus, channel, on, off):
    reg_base = 0x06 + 4 * channel
    data = [on & 0xFF, on >> 8, off & 0xFF, off >> 8]
    bus.write_i2c_block_data(PCA_ADDRESS, reg_base, data)

def move_to_zone(zone_id):
    if zone_id not in ZONE_ANGLES:
        raise ValueError(f"Invalid zone: {zone_id}")
    
    pan_angle, tilt_angle = ZONE_ANGLES[zone_id]
    pan_pwm = angle_to_pwm(pan_angle)
    tilt_pwm = angle_to_pwm(tilt_angle)

    with smbus2.SMBus(I2C_BUS) as bus:
        # Initialize PCA9685
        bus.write_byte_data(PCA_ADDRESS, 0x00, 0x00)  # MODE1 register, normal mode
        bus.write_byte_data(PCA_ADDRESS, 0xFE, 0x79)  # PRE_SCALE for 50Hz

        # Write PWM values
        set_pwm(bus, PAN_CHANNEL, 0, pan_pwm)
        set_pwm(bus, TILT_CHANNEL, 0, tilt_pwm)

    print(f"[ZoneController] Moved to Zone {zone_id}: Pan={pan_angle}, Tilt={tilt_angle}")
    time.sleep(1)