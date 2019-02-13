import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(26, GPIO.BOTH)
def my_callback(channel):
    print('DOWN ', channel)
GPIO.add_event_callback(26, my_callback)
while True:
    # if GPIO.input(26) == GPIO.LOW:
    #     print ("Switch pressed DOWN.")
    # else:
    #     print ("Switch pressed UP.")
    time.sleep(0.5)
