import seeed_si114x
import RPi.GPIO as GPIO
import time
from influxdb import InfluxDBClient


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
    with open('/home/pi/plant-rotator/current_section.txt', 'r') as f:
        return int(f.readline())


def read_metric():
    SI1145 = seeed_si114x.grove_si114x()
    return SI1145.ReadVisible
    # print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR))


def save_metric(section, value):
    client = InfluxDBClient('localhost', 8086, 'pi', 'password', 'plant')
    point = {
        'measurement': 'sunlight-%s' % section,
        'fields': {
            'value': value
        }
    }
    client.write_points([point])


def update_section_value(sun_value, section):
    with open('/home/pi/plant-rotator/section_sunlight.txt', 'r') as f:
        starting_value = int(f.readline())
    new_value = starting_value + max(sun_value - 265, 0)
    if new_value > 100000:
        next_section = (section + 1) % 4
        with open('/home/pi/plant-rotator/current_section.txt', 'w') as f:
            f.write('%s\n' % next_section)
        new_value = 0
    with open('/home/pi/plant-rotator/section_sunlight.txt', 'w') as f:
        f.write('%s\n' % new_value)


if __name__  == '__main__':
    section = get_section()
    sun_value = read_metric()
    save_metric(section, sun_value)
    update_section_value(sun_value, section)
