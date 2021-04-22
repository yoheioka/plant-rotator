import RPi.GPIO as GPIO
import time
from influxdb import InfluxDBClient


THRESH = 265
ROTATE_THRESH = 50000


def rotate():
    GPIO.setmode(GPIO.BOARD)
    control_pins = [7,11,13,15]
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    halfstep_seq = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
    ]
    for i in range(128):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            time.sleep(0.002)
    GPIO.cleanup()


def get_section():
    with open('/home/pi/plant-rotator/section_sunlight.txt', 'r') as f:
        section_value = int(f.readline())
    with open('/home/pi/plant-rotator/current_section.txt', 'r') as f:
        section = int(f.readline())

    if section_value > ROTATE_THRESH:
        section = (section + 1) % 4
        with open('/home/pi/plant-rotator/current_section.txt', 'w') as f:
            f.write('%s\n' % section)
        section_value = 0
        rotate()
    return section, section_value


def read_metric():
    # the rotation has to happen before this import
    import seeed_si114x
    SI1145 = seeed_si114x.grove_si114x()
    return SI1145.ReadVisible


def save_metric(metric, value):
    client = InfluxDBClient('localhost', 8086, 'pi', 'password', 'plant')
    point = {
        'measurement': metric,
        'fields': {
            'value': value
        }
    }
    client.write_points([point])


def update_section_value(new_value, section):
    with open('/home/pi/plant-rotator/section_sunlight.txt', 'w') as f:
        f.write('%s\n' % new_value)


if __name__  == '__main__':
    section, section_value = get_section()
    sun_value = read_metric()
    delta = max(sun_value - THRESH, 0)

    save_metric('sunlight-%s' % section, sun_value)
    save_metric('sunlight-delta-%s' % section, delta)

    update_section_value(section_value + delta, section)
