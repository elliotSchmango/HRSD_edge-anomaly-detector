import smbus2
import time

# Constants
I2C_BUS = 1
PCA_ADDRESS = 0x40
PAN_CHANNEL = 0
TILT_CHANNEL = 1

# Zone mapping
ZONE_ANGLES = {
    1: (60, 120), 2: (90, 120), 3: (120, 120),
    4: (60, 90),  5: (90, 90),  6: (120, 90),
    7: (60, 60),  8: (90, 60),  9: (120, 60)
}

# Open persistent I2C connection
bus = smbus2.SMBus(I2C_BUS)

def angle_to_pwm(angle):
    return int((angle / 180.0) * 450 + 150)

def set_pwm(channel, on, off):
    reg = 0x06 + 4 * channel
    data = [on & 0xFF, on >> 8, off & 0xFF, off >> 8]
    bus.write_i2c_block_data(PCA_ADDRESS, reg, data)

# Track if already initialized
pca_initialized = False

def init_pca():
    global pca_initialized
    if not pca_initialized:
        bus.write_byte_data(PCA_ADDRESS, 0x00, 0x00)  # MODE1
        bus.write_byte_data(PCA_ADDRESS, 0xFE, 0x79)  # PRE_SCALE
        time.sleep(0.01)
        pca_initialized = True

def move_to_zone(zone_id):
    if zone_id not in ZONE_ANGLES:
        raise ValueError(f"Invalid zone: {zone_id}")

    init_pca()

    pan_angle, tilt_angle = ZONE_ANGLES[zone_id]
    pan_pwm = angle_to_pwm(pan_angle)
    tilt_pwm = angle_to_pwm(tilt_angle)

    set_pwm(PAN_CHANNEL, 0, pan_pwm)
    set_pwm(TILT_CHANNEL, 0, tilt_pwm)

    print(f"[ZoneController] Zone {zone_id}: Pan={pan_angle}, Tilt={tilt_angle}")
    time.sleep(1)