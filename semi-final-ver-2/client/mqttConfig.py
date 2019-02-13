class MqttConfig:
    server_broker_address='192.168.1.51'
    port='1883'
    #sensor config
    sensorTopic="cds/sensor"
    commandTopic="cds/command"
    caseTopic="cds/case"
    servoTopic="cds/server/servo"
    newRoundTopic="cds/newRound"
    newCaseTopic="cds/case"
    checkSensorStopTopic="cds/server/sensor6"
    checkStopFor5SecondTopic='cds/sensor6/stop'
    isSendMessageSensor5Topic='cds/sensor5/log'
    retryTopic='cds/retry'
    
    #servo config
    servoCommandTopic="cds/servo/command"
    commandTopic="cds/command"
    servoStateTopic="cds/servo/state"
    servoNewRoundTopic="cds/servo/newRound"

    # checkLife
    checkLifeTopic='cds/checkLife'
