#pip install rpi.gpio
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor

#while True:
def geMotionData():
    i=GPIO.input(8)
    return i  # 1=motion detected, 0=Not detected
    