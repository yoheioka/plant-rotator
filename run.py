import seeed_si114x
from influxdb import InfluxDBClient


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


if __name__  == '__main__':
    section = get_section()
    sun_value = read_metric()
    save_metric(section, sun_value)

