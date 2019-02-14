import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(15, gpio.OUT)
gpio.output(15, gpio.LOW)
time.sleep(1)
gpio.output(15, gpio.HIGH)
