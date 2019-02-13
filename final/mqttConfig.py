class MqttConfig:
    server_broker_address='192.168.1.51'
    port='1883'
    #sensor config
    sensorTopicFinal="cds/sensor/final"
    commandTopic="cds/command"
    caseTopic="cds/case"
    servoTopic="cds/server/servo"
    isSendMessageSensor5TopicFinal='cds/sensor5/log/final'
    retryTopicFinal='cds/retry/final'

    #servo config
    servoCommandTopic="cds/servo/command/final"
    servoStateTopic="cds/servo/state"
    checkLifeTopic="cds/checkLife"

    
