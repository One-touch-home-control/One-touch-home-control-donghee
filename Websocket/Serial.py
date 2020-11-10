import serial
import time

message = 'led'
i = 0

ser = serial.Serial('/dev/ttyACM1', 9600)

# ser.write(message.encode())
# while True:

while True:
    if(ser.readable()):
        res = ser.readline()
        ser.write(message.encode())