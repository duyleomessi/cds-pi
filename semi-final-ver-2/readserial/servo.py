import RPi.GPIO as IO
import time
IO.setwarnings(False)          
IO.setmode(IO.BCM)
IO.setup(21, IO.OUT)        # initialize GPIO19 as an output
p = IO.PWM(21, 50)          # GPIO19 as PWM output, with 50Hz frequency
# generate PWM signal with 7.5% duty cycle
p.start(7.5)
while 1:                    # execute loop forever change duty cycle for getting the servo position to 90
    p.ChangeDutyCycle(7.5)
    time.sleep(1)           # sleep for 1 second change duty cycle for getting the servo position to 180
    p.ChangeDutyCycle(12.5)
    time.sleep(1)           # sleep for 1 second change duty cycle for getting the servo position to 0
    p.ChangeDutyCycle(2.5)
    time.sleep(1)           # sleep for 1 second
