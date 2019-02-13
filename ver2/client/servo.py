import sys
import time
import threading
import RPi.GPIO as GPIO
from mqttConfig import *
from servoConfig import *
from stadiumConfig import *
import json
import random

import paho.mqtt.client as mqtt

servo1 = SERVO_SIGNAL_1()
servo2 = SERVO_SIGNAL_2()

def handle_message_command(client, userdata, message):
    print("message command recieve: ", str(message.payload.decode("utf-8")))
    commandData = json.loads(message.payload)
    if ("RACE_START_1" in commandData['command']):
        randomServo()

def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")

def handle_message_servo(client, userdata, message):
    print("message recieve: ", str(message.payload.decode("utf-8")))
    json_data = json.loads(message.payload)
    print(json_data)
    if stadiumConfig.STADIUM == json_data['stadium']:
        if json_data['servo'] == 1:
            setAngle(pwm1, servo1, getattr(servo1, json_data['angle']))
        elif json_data['servo'] == 2:
            setAngle(pwm2, servo2, getattr(servo2, json_data['angle']))
        else:
            print("Deo lam gi")

def handle_new_case(client, userdata, message):
    print("message recieve: ", str(message.payload.decode("utf-8")))
    json_data = json.loads(message.payload)
    print(json_data)
    if json_data['stadium'] == stadiumConfig.STADIUM:
        randomServo()

def handle_servo_new_round(client, userdata, message):
    print("message recieve: ", str(message.payload.decode("utf-8")))
    json_data = json.loads(message.payload)
    print(json_data)
    if json_data['stadium'] == stadiumConfig.STADIUM:
        randomServo()

mqttConfig = MqttConfig()
stadiumConfig = StadiumConfig()
client = mqtt.Client()

#handle connection and message
client.on_connect = handle_connect
client.connect(mqttConfig.server_broker_address, mqttConfig.port)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servo1.SERVO_PIN, GPIO.OUT)      # initialize GPIO19 as an output
pwm1 = GPIO.PWM(servo1.SERVO_PIN, 50)          # GPIO19 as PWM output, with 50Hz frequency
pwm1.start(0)

GPIO.setup(servo2.SERVO_PIN, GPIO.OUT)      # initialize GPIO19 as an output
pwm2 = GPIO.PWM(servo2.SERVO_PIN, 50)          # GPIO19 as PWM output, with 50Hz frequency
pwm2.start(0)

def setAngle(pwm, servo, angle):
    # duty = angle / 18 + 2
    print("Quay servo ", servo )
    GPIO.output(servo.SERVO_PIN, True)
    pwm.ChangeDutyCycle(angle)
    time.sleep(1)
    GPIO.output(servo.SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

def randomServo():
    random1 = random.randint(1, 2)
    if random1 == 1:
        setAngle(pwm1, servo1, servo1.LEFT)
        publishServoState(1, "LEFT")
    elif random1 == 2:
        setAngle(pwm1, servo1, servo1.RIGHT)
        publishServoState(1, "RIGHT")
        
    random2 = random.randint(1, 2)
    if random2 == 1:
        # setAngle(pwm2, servo2, servo2.LEFT)
        publishServoState(2, "LEFT")
    elif random2 == 2:
        # setAngle(pwm2, servo2, servo2.RIGHT)
        publishServoState(2, "RIGHT")

def publishServoState(servo, state):
    data = {"stadium": stadiumConfig.STADIUM, "servo": servo, "state": state}
    json_data = json.dumps(data)
    client.publish(mqttConfig.servoStateTopic, json_data)

while True:
    client.loop_start()
    client.subscribe(mqttConfig.servoCommandTopic)
    client.message_callback_add(mqttConfig.servoCommandTopic, handle_message_servo)
    client.subscribe(mqttConfig.commandTopic)
    client.message_callback_add(mqttConfig.commandTopic, handle_message_command)
    client.subscribe(mqttConfig.servoNewRoundTopic)
    client.message_callback_add(mqttConfig.servoNewRoundTopic, handle_servo_new_round)
    client.subscribe(mqttConfig.newCaseTopic)
    client.message_callback_add(mqttConfig.newCaseTopic, handle_new_case)
    time.sleep(0.1)
    
