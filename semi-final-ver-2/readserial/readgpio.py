import RPi.GPIO as GPIO
from enum import Enum
import time

class SENSOR(Enum):
    SENSOR_1 = 5
    SENSOR_2 = 6
    SENSOR_3 = 13
    SENSOR_4 = 19
    SENSOR_5 = 26
class SWITCH(Enum):
    START = 2
class SERVO(Enum):
    SERVO_1 = 21

sensorname = {}
sensorname[SENSOR.SENSOR_1] = "P1"
sensorname[SENSOR.SENSOR_2] = "P2"
sensorname[SENSOR.SENSOR_3] = "P3"
sensorname[SENSOR.SENSOR_4] = "P4"
sensorname[SENSOR.SENSOR_5] = "P5"

Stadium = "G" # "Green"
START_TIME = time.time()

#Init GPIO
chan_list = [SENSOR.SENSOR_1, SENSOR.SENSOR_2, SENSOR.SENSOR_3, SENSOR.SENSOR_4, SENSOR.SENSOR_5]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def gpio_sensor_callback(channel):
    global START_TIME
    timestamp = time.time()
    runtime = timestamp - START_TIME
    print("%s:%s:%s\n" % (Stadium, runtime, sensorname[channel]))

#GPIO.add_event_detect(SENSOR.SENSOR_5, GPIO.BOTH)
#GPIO.add_event_callback(SENSOR.SENSOR_5, gpio_sensor_callback)

while True:
    val = GPIO.input(SENSOR.SENSOR_5)
    if val == 0:
        print(val)
    time.sleep(0.05)