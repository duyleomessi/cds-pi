import sys
import time
import RPi.GPIO as GPIO
from mqttConfig import *
from sensorConfig import *
from stadiumConfig import *
import json

import paho.mqtt.client as mqtt

sensor = SENSOR()

sensorname = {}
sensorname[sensor.SENSOR_6] = "6"

def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")

                    
mqttConfig = MqttConfig()
stadiumConfig = StadiumConfig()
client = mqtt.Client()

# handle connection and message
client.on_connect = handle_connect
# client.on_message = handle_message
client.connect(mqttConfig.server_broker_address, mqttConfig.port)

#Init GPIO
chan_list = [sensor.SENSOR_6]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def send_check_message(stadium, channel, isStop): 
    # khi xe den sensor 6 se gui 1 ban tin len server de kich hoat dem 5s
    if isStop == 0:
        data = {'stadium': stadiumConfig.STADIUM, 'channel': channel, 'isStop': 'false'}
    elif isStop == 1:
        data = {'stadium': stadiumConfig.STADIUM, 'channel': channel, 'isStop': 'true'}
    json_data = json.dumps(data)
    client.publish(mqttConfig.checkSensorStopTopic, json_data)

def handle_message_command(client, userdata, message):
    global startRace
    commandData = json.loads(message.payload)
    if ("RACE_START_1" in commandData['command']):
        startRace = True 
    elif("RACE_STOP_1" in commandData['command']):
        startRace = False
    elif("RACE_RESET_1" in commandData['command']):
        startRace = False
        
startRace = False

count = 0
def gpio_sensor_callback(channel):
    global sensor
    global sensorname
    global count
    sensor_index = sensor.index(channel)
    count += 1

    if channel == sensor.SENSOR_6 and startRace:
       if GPIO.input(26) == 0:
            print("%s:%s:%d" % (stadiumConfig.STADIUM, sensorname[channel], count))
            send_check_message(stadiumConfig.STADIUM, sensorname[channel], 1)
       elif GPIO.input(26) == 1:
            send_check_message(stadiumConfig.STADIUM, sensorname[channel], 0)


# callback for sensor detect
GPIO.add_event_detect(sensor.SENSOR_6, GPIO.BOTH)
GPIO.add_event_callback(sensor.SENSOR_6, gpio_sensor_callback)

while True:
    client.loop_start()
    # client.subscribe(mqttConfig.checkStopFor5SecondTopic)
    # client.message_callback_add(mqttConfig.checkStopFor5SecondTopic, handle_message_check_stop)
    client.subscribe(mqttConfig.commandTopic)
    client.message_callback_add(mqttConfig.commandTopic, handle_message_command)
    time.sleep(0.2)

GPIO.cleanup()
