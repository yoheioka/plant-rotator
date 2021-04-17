import RPi.GPIO as GPIO
import time

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


def update_section():
    with open('/home/pi/plant-rotator/current_section.txt', 'r') as f:
        num = int(f.readline())
        next = (num + 1) % 4
    with open('/home/pi/plant-rotator/current_section.txt', 'w') as f:
        f.write('%s\n' % next)

if __name__ == '__main__':
    rotate()
    update_section()
