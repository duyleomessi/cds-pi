class SENSOR1:
    SENSOR_1 = 5
    SENSOR_2 = 6
    SENSOR_3 = 13
    SENSOR_4 = 19 
    SENSOR_5 = 26

    @classmethod
    def index(cls, val):
        if val == 5:
            return 0
        if val == 6:
            return 1
        if val == 13:
            return 2
        if val == 19:
            return 3
        if val == 26:
            return 4

class SENSOR2:
    SENSOR_1 = 5
    SENSOR_2 = 6
    SENSOR_3 = 19
    SENSOR_4 = 13
    SENSOR_5 = 26

    @classmethod
    def index(cls, val):
        if val == 5:
            return 0
        if val == 6:
            return 1
        if val == 19:
            return 2
        if val == 13:
            return 3
        if val == 26:
            return 4

class SENSOR3:
    SENSOR_1 = 6
    SENSOR_2 = 5
    SENSOR_3 = 13
    SENSOR_4 = 19 
    SENSOR_5 = 26

    @classmethod
    def index(cls, val):
        if val == 6:
            return 0
        if val == 5:
            return 1
        if val == 13:
            return 2
        if val == 19:
            return 3
        if val == 26:
            return 4

class SENSOR4:
    SENSOR_1 = 6
    SENSOR_2 = 5
    SENSOR_3 = 19
    SENSOR_4 = 13 
    SENSOR_5 = 26

    @classmethod
    def index(cls, val):
        if val == 6:
            return 0
        if val == 5:
            return 1
        if val == 19:
            return 2
        if val == 13:
            return 3
        if val == 26:
            return 4


class SWITCH:
    START = 20

class SERVO_START:
    SERVO_PIN = 21
    START_ANGLE = 3 
    STOP_ANGLE = 7.5 

