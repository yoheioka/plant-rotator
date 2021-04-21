import RPi.GPIO as GPIO
import time


def read_metric():
    import seeed_si114x
    SI1145 = seeed_si114x.grove_si114x()
    print(SI1145.ReadVisible)
    return SI1145.ReadVisible


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


if __name__ == '__main__':
    rotate()
    read_metric()
