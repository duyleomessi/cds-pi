import sys
import time
import threading
import socket
import RPi.GPIO as GPIO
from enum import Enum
from myconfig import *

sensorname = {}
sensorname[SENSOR.SENSOR_1] = "P1"
sensorname[SENSOR.SENSOR_2] = "P2"
sensorname[SENSOR.SENSOR_3] = "P3"
sensorname[SENSOR.SENSOR_4] = "P4"
sensorname[SENSOR.SENSOR_5] = "P5"

isSend = [0, 1, 1, 1, 1]

START_TIME = time.time()

#Init GPIO
chan_list = [SENSOR.SENSOR_1, SENSOR.SENSOR_2, SENSOR.SENSOR_3, SENSOR.SENSOR_4, SENSOR.SENSOR_5, SWITCH.START]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO.SERVO_1, GPIO.OUT)      # initialize GPIO19 as an output
pwm = GPIO.PWM(SERVO.SERVO_1, 50)          # GPIO19 as PWM output, with 50Hz frequency
pwm.start(SERVO.STOP_ANGLE)

#Init TCP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (SERVER.IP, SERVER.PORT)

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

while True:
    try:
        connect()
        break
    except:
        print('False to conect to server')
        time.sleep(1)

def reset_round():
    global START_TIME, isSend
    isSend = [0, 1, 1, 1, 1]
    START_TIME = time.time()

def receive_message(threadName):
    global START_TIME, isSend
    data = ''
    while True:
        try:
            tmp = sock.recv(32)
            tmp = tmp.decode("utf-8")
            data += tmp
            if '\n' in tmp:
                # xu ly du lieu tu server (start)
                if 'START_ROUND_' + ROUND in data:
                    print(data)
                    pwm.ChangeDutyCycle(SERVO.START_ANGLE)
                    reset_round()
                if 'STOP_ROUND' + ROUND in data:
                    print(data)
                    pwm.ChangeDutyCycle(SERVO.STOP_ANGLE)
                    reset_round()
                if 'RESET_ROUND_%s' % ROUND in data:
                    print(data)
                    pwm.ChangeDutyCycle(SERVO.STOP_ANGLE)
                    reset_round()
                data = ''
        except:
            print('ERROR\n')
            time.sleep(1)
            connect()

def send_message(data):
    count = 0
    while True:
        try:
            count += 1
            sock.sendall(data.encode())
            break
        except:
            time.sleep(1)
            connect()
            if count > 2:
                print("Send message: %s [FALSE]" % data)
                break

def gpio_sensor_callback(channel):
    global START_TIME, isSend
    timestamp = time.time()
    runtime = timestamp - START_TIME
    sensor_index = SENSOR.index(channel)

    if isSend[sensor_index] == 0:
        print("%s:%s:%s" % (STADIUM, sensorname[channel], runtime))
        send_message("%s:%s:%s" % (STADIUM, sensorname[channel], runtime))
        isSend[sensor_index] = 1
        isSend[((sensor_index + 1)%5)] = 0
        if channel == SENSOR.SENSOR_5 and ROUND == '1':
            START_TIME = time.time()


GPIO.add_event_detect(SENSOR.SENSOR_1, GPIO.BOTH)
GPIO.add_event_callback(SENSOR.SENSOR_1, gpio_sensor_callback)
GPIO.add_event_detect(SENSOR.SENSOR_2, GPIO.BOTH)
GPIO.add_event_callback(SENSOR.SENSOR_2, gpio_sensor_callback)
GPIO.add_event_detect(SENSOR.SENSOR_3, GPIO.BOTH)
GPIO.add_event_callback(SENSOR.SENSOR_3, gpio_sensor_callback)
GPIO.add_event_detect(SENSOR.SENSOR_4, GPIO.BOTH)
GPIO.add_event_callback(SENSOR.SENSOR_4, gpio_sensor_callback)
GPIO.add_event_detect(SENSOR.SENSOR_5, GPIO.BOTH)
GPIO.add_event_callback(SENSOR.SENSOR_5, gpio_sensor_callback)

class myThread(threading.Thread):
    def __init__(self, threadID, name, function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.function = function
    def run(self):
        print("Starting %s" % self.name)
        self.function(self.name)
        print("Exiting " + self.name)

# Create new threads
thread_rmessage = myThread(2, "Thread-rmessage", receive_message)

# Start new Threads
thread_rmessage.start() 
pre_state = 0
count = 0
start_state = 0

while True:
    cur_state = GPIO.input(SWITCH.START)
    if pre_state == cur_state:
        count += 1
    pre_state = cur_state
    if count > 3:
        #print(cur_state)
        count = 0
        if start_state != cur_state:
            START_TIME = time.time()
            print('Run servo')
            if start_state == 0: # STOP
                pwm.ChangeDutyCycle(SERVO.STOP_ANGLE)
                reset_round()
            else:                # START
                pwm.ChangeDutyCycle(SERVO.START_ANGLE)
                send_message("%s:%s:%s" % (STADIUM, 'START', 'START'))
                reset_round()
        start_state = cur_state
    time.sleep(0.2)

pwm.stop()
GPIO.cleanup()
