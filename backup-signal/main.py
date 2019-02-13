import RPi.GPIO as GPIO
import time
from myconfig import *

servoSignal1 = SERVO_SIGNAL_1()
servoSignal2 = SERVO_SIGNAL_2()

# setup for servo signal
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(servoSignal1.SERVO_PIN, GPIO.OUT)      # initialize GPIO19 as an output
pwm1 = GPIO.PWM(servoSignal1.SERVO_PIN, 50)          # GPIO19 as PWM output, with 50Hz frequency
pwm1.start(servoSignal1.STRAIGH)
GPIO.setup(servoSignal2.SERVO_PIN, GPIO.OUT)      # initialize GPIO19 as an output
pwm2 = GPIO.PWM(servoSignal2.SERVO_PIN, 50)          # GPIO19 as PWM output, with 50Hz frequency
pwm2.start(servoSignal2.STRAIGH)

while True:
    userInput = int(raw_input("Enter the number: ") )
    # truong hop 1 sensor 1
    #if userInput == 11:
    #    pwm1.ChangeDutyCycle(servoSignal1.RIGHT)
    #    time.sleep(0.5)
    #    pwm1.ChangeDutyCycle(servoSignal1.STRAIGH_LEFT) 
    #    pwm2.ChangeDutyCycle(servoSignal2.LEFT)
    ## truong hop 1 sensor 3
    #elif userInput == 13:
    #    pwm2.ChangeDutyCycle(servoSignal2.RIGHT)  
    #    time.sleep(0.5)
    #    pwm2.ChangeDutyCycle(servoSignal2.STRAIGH_LEFT)
    #
    ## truong hop 2 sensor 1
    #if userInput == 21:
    #    pwm1.ChangeDutyCycle(servoSignal1.RIGHT)
    #    time.sleep(0.5)
    #    pwm1.ChangeDutyCycle(servoSignal1.STRAIGH_LEFT) 
    #    pwm2.ChangeDutyCycle(servoSignal2.RIGHT)
    ## truong hop 2 sensor 3
    #elif userInput == 23:
    #    pwm2.ChangeDutyCycle(servoSignal2.LEFT)  
    #    time.sleep(0.5)
    #    pwm2.ChangeDutyCycle(servoSignal2.STRAIGH_RIGH)

    ## truong hop 3 sensor 1
    #if userInput == 31:
    #    pwm1.ChangeDutyCycle(servoSignal1.LEFT)
    #    time.sleep(0.5)
    #    pwm1.ChangeDutyCycle(servoSignal1.STRAIGH_RIGH)
    #    pwm2.ChangeDutyCycle(servoSignal2.LEFT)
    ## truong hop 3 sensor 3
    #elif userInput == 33:
    #    pwm2.ChangeDutyCycle(servoSignal2.RIGHT)  
    #    time.sleep(0.5)
    #    pwm2.ChangeDutyCycle(servoSignal2.STRAIGH_LEFT)
    #
    ## truong hop 4 sensor 1
    #if userInput == 41:
    #    pwm1.ChangeDutyCycle(servoSignal1.LEFT)
    #    time.sleep(0.5)
    #    pwm1.ChangeDutyCycle(servoSignal1.STRAIGH_RIGH)
    #    pwm2.ChangeDutyCycle(servoSignal2.RIGHT)
    #elif userInput == 43:
    #    pwm2.ChangeDutyCycle(servoSignal2.LEFT)  
    #    time.sleep(0.5)
    #    pwm2.ChangeDutyCycle(servoSignal2.STRAIGH_RIGH)

    if userInput == 11:
        pwm1.ChangeDutyCycle(servoSignal1.LEFT)
    elif userInput == 12:
        pwm1.ChangeDutyCycle(servoSignal1.RIGHT)
        time.sleep(0.5)
        pwm1.ChangeDutyCycle(servoSignal1.STRAIGH_LEFT)
    elif userInput == 13:
        pwm1.ChangeDutyCycle(servoSignal1.LEFT)
        time.sleep(0.5)
        pwm1.ChangeDutyCycle(servoSignal1.STRAIGH_RIGH)
    elif userInput == 14:
        pwm1.ChangeDutyCycle(servoSignal1.RIGHT)
    
    elif userInput == 31:
        pwm2.ChangeDutyCycle(servoSignal2.LEFT)
    elif userInput == 32:
        pwm2.ChangeDutyCycle(servoSignal2.RIGHT)
        time.sleep(0.5)
        pwm2.ChangeDutyCycle(servoSignal2.STRAIGH_LEFT)
    elif userInput == 33:
        pwm2.ChangeDutyCycle(servoSignal2.LEFT)
        time.sleep(0.5)
        pwm2.ChangeDutyCycle(servoSignal2.STRAIGH_RIGH)
    elif userInput == 34:
        pwm2.ChangeDutyCycle(servoSignal2.RIGHT)

    else:
        print("Invalid input")
