import sys
import time
import RPi.GPIO as GPIO
from mqttConfig import *
from sensorConfig import *
from stadiumConfig import *
import random
import json

import paho.mqtt.client as mqtt

switch = SWITCH()
servoStart = SERVO_START()
sensor = SENSOR1()
startRace = False

sensorname = {}
sensorname[sensor.SENSOR_1] = "1"
sensorname[sensor.SENSOR_2] = "2"
sensorname[sensor.SENSOR_3] = "3"
sensorname[sensor.SENSOR_4] = "4"
sensorname[sensor.SENSOR_5] = "5"


def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")

def handle_message_command(client, userdata, message):
    global startRace
    print("message command recieve: ", str(message.payload.decode("utf-8")))
    commandData = json.loads(message.payload)
    if ("RACE_START_2" in commandData['command']):
        setAngle(pwm, servoStart, servoStart.START_ANGLE)
        startRace = True
        reset_round()
    if ("RACE_STOP_2" in commandData['command']):
        setAngle(pwm, servoStart, servoStart.STOP_ANGLE)
        startRace = False
        reset_round()
    if ("RACE_RESET_2" in commandData['command']):
        setAngle(pwm, servoStart, servoStart.STOP_ANGLE)
        startRace = False
        reset_round()

def handle_message_retry(client, userdata, message):
        print("message retry recieve: ", str(message.payload.decode("utf-8")))
        data = json.loads(message.payload)
        if stadiumConfig.STADIUM == data['stadium'] and data['state'] == 'open':
            setAngle(pwmStart, servoStart, servoStart.START_ANGLE)
            #send_message("%s:%s:%s" % (stadiumConfig.STADIUM, 'START', 'START'))
            reset_round()
        elif stadiumConfig.STADIUM == data['stadium'] and data['state'] == 'close':
            setAngle(pwmStart, servoStart, servoStart.STOP_ANGLE)
            #send_message("%s:%s:%s" % (stadiumConfig.STADIUM, 'START', 'START'))
            reset_round()
            
# khi di qua sensor 5 o vong 2 thi gui ban tin
def handle_message_log_sensor_5(client, userdata, message):
    print("message sensor 5 recieve: ", str(message.payload.decode("utf-8")))
    data = json.loads(message.payload) 
    if stadiumConfig.STADIUM == data['stadium']:
        isSend[4] = 0

mqttConfig = MqttConfig()
stadiumConfig = StadiumConfig()
client = mqtt.Client()

def handle_message_new_round(client, userdata, message):
    print("message new round recieve: ", str(message.payload.decode("utf-8")))
    data = json.loads(message.payload) 
    if stadiumConfig.STADIUM == data['stadium']:
        START_TIME = time.time()
        reset_round()

# handle connection and message
client.on_connect = handle_connect
# client.on_message = handle_message
client.connect(mqttConfig.server_broker_address, mqttConfig.port)

isSend = [0, 0, 0, 0, 1]

START_TIME = time.time()

#Init GPIO
chan_list = [sensor.SENSOR_1, sensor.SENSOR_2, sensor.SENSOR_3, sensor.SENSOR_4, sensor.SENSOR_5, switch.START]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def reset_round():
    print("Reset round")
    global START_TIME, isSend
    isSend = [0, 0, 0, 0, 1]
    START_TIME = time.time()

def send_message(stadium, channel, runtime):
    data = {'stadium': stadium, 'channel': channel, 'runtime': runtime}
    json_data =  json.dumps(data)
    client.publish(mqttConfig.sensorTopicFinal, json_data)

def send_servo_message(stadium, servo, channel):
    data = {'stadium': stadium, 'servo': servo ,'channel': channel}
    json_data = json.dumps(data)
    client.publish(mqttConfig.servoTopic, json_data)

def setAngle(pwm, servo, angle):
    # duty = angle / 18 + 2
    GPIO.output(servo.SERVO_PIN, True)
    pwm.ChangeDutyCycle(angle)
    time.sleep(1)
    GPIO.output(servo.SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

# setup for servo start
GPIO.setup(servoStart.SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(servoStart.SERVO_PIN, 50)
pwm.start(servoStart.STOP_ANGLE)

def requestNewCase(): 
    data = {'stadium': stadiumConfig.STADIUM}
    json_data = json.dumps(data)
    client.publish(mqttConfig.newCaseTopic, json_data)

def gpio_sensor_callback(channel):
    global START_TIME, isSend, isTouch
    timestamp = time.time()
    runtime = timestamp - START_TIME
    global sensor
    global sensorname
    sensor_index = sensor.index(channel)

    #print(isSend[4])
    if isSend[sensor_index] == 0 and startRace:
        print("%s:%s:%s" % (stadiumConfig.STADIUM, sensorname[channel], runtime))
        if channel != sensor.SENSOR_5:
            send_message(stadiumConfig.STADIUM, sensorname[channel], runtime)
        # xe di qua sensor 5 2 lan het vong 1 va het vong 2
        # ta chi gui du lieu khi xe di qua sensor 5 sau vong 2
        elif channel == sensor.SENSOR_5:  #and isSendMessageSensor5:
            send_message(stadiumConfig.STADIUM, sensorname[channel], runtime)
            # START_TIME = time.time()
            # reset_round()
            # requestNewCase()

# callback for sensor detect
GPIO.add_event_detect(sensor.SENSOR_1, GPIO.FALLING)
GPIO.add_event_callback(sensor.SENSOR_1, gpio_sensor_callback)
GPIO.add_event_detect(sensor.SENSOR_2, GPIO.FALLING)
GPIO.add_event_callback(sensor.SENSOR_2, gpio_sensor_callback)
GPIO.add_event_detect(sensor.SENSOR_3, GPIO.FALLING)
GPIO.add_event_callback(sensor.SENSOR_3, gpio_sensor_callback)
GPIO.add_event_detect(sensor.SENSOR_4, GPIO.FALLING)
GPIO.add_event_callback(sensor.SENSOR_4, gpio_sensor_callback)
GPIO.add_event_detect(sensor.SENSOR_5, GPIO.FALLING)
GPIO.add_event_callback(sensor.SENSOR_5, gpio_sensor_callback)

pre_state = 0
count = 0
start_state = 0

while True:
    client.loop_start()
    client.subscribe(mqttConfig.commandTopic)
    client.message_callback_add(mqttConfig.commandTopic, handle_message_command)
    client.subscribe(mqttConfig.isSendMessageSensor5TopicFinal)
    client.message_callback_add(mqttConfig.isSendMessageSensor5TopicFinal, handle_message_log_sensor_5)
    client.subscribe(mqttConfig.retryTopicFinal)
    client.message_callback_add(mqttConfig.retryTopicFinal, handle_message_retry)


    time.sleep(0.2)

    cur_state = GPIO.input(switch.START) 
    # if switch is pressed, cur_state = 0 
    # print(cur_state)
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
                # pwm.ChangeDutyCycle(servo.STOP_ANGLE)
                setAngle(pwm, servoStart, servoStart.STOP_ANGLE)
                reset_round()
            else:                # START
                # requestNewCase()
                # pwm.ChangeDutyCycle(servo.START_ANGLE)
                setAngle(pwm, servoStart, servoStart.START_ANGLE)
                #send_message("%s:%s:%s" % (stadiumConfig.STADIUM, 'START', 'START'))
                reset_round()
        start_state = cur_state
    time.sleep(0.2)

pwm.stop()
GPIO.cleanup()
