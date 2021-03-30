import RPi.GPIO as GPIO
import time


servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servoPIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servoPIN, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # p.ChangeDutyCycle(5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(7.5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(10)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(12.5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(10)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(7.5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(2.5)
        # time.sleep(0.5)
        set_angle(90)
        time.sleep(0)
        set_angle(90)
        time.sleep(0)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
