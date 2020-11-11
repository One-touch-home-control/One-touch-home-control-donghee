import RPi.GPIO as g
from time import sleep
from RPIO import PWM



SERVO_PIN = 12

# g.setmode(g.BCM)
# g.setup(SERVO_PIN, g.OUT)
# servoPWM = g.PWM(SERVO_PIN, 50)
# servoPWM.start(0)
# 
# servoPWM.ChangeDutyCycle(12)
# sleep(1)
# 
# servoPWM.ChangeDutyCycle(7)
# while True:
#     sleep(1)
# 
# 
# g.cleanup()

servo = PWM.Servo()

servo.ser_servo(SERVO_PIN, 1200)

sleep(10)

servo.stop_servo(SERVO_PIN)