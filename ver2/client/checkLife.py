import paho.mqtt.client as mqtt
from mqttConfig import *
from stadiumConfig import *
import json
import time

def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed");

def handle_disconnect(client, userdata, flags, rc):
    print("disconnect")

client = mqtt.Client(client_id="pi control san do 1 ", clean_session=False)
stadiumConfig = StadiumConfig()
mqttConfig = MqttConfig()

client.connect(mqttConfig.server_broker_address , mqttConfig.port)
client.on_connect = handle_connect

while True:
    client.loop_start()
    name = stadiumConfig.NAME
    function = stadiumConfig.FUNCTION 
    data = {'name': name, 'function': function} 
    json_data = json.dumps(data)
    client.publish(mqttConfig.checkLifeTopic, json_data)
    time.sleep(5)

