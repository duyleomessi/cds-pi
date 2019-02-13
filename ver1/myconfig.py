from enum import Enum

STADIUM = "G1" # "Green" G1,R1,G2,R2
ROUND  = '1' # 1 or 2
class SERVER(Enum):
    IP = '10.3.9.55'
    PORT = 8080
class SENSOR(Enum):
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

class SWITCH(Enum):
    START = 20
class SERVO(Enum):
    SERVO_1 = 21
    START_ANGLE = 2.5
    STOP_ANGLE = 7.0
