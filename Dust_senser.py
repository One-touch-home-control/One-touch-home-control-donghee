import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

microDustData = 0.0
microDustCount = 0
while True:
    try:
        for i in range(10):
            while True:
                if(ser.in_waiting >0):
                    line = ser.readline()
                    data = str(line)
#                     print(data)
                    data1 = data.split("e", 1)[1]
#                     print(data1)
                    data2 = data1.split("f", 1)[0]
                    
#                     print(data2)
#                     print(len(line))
                    try:
                        readData = int(data2)
                    except:
                        continue
#                     print(readData)
#                     print()
                    if readData > 10 and readData < 500:
                        microDustData += readData
                        microDustCount += 1
                    ser.flush()
                    break
        if microDustCount == 0:
            continue
        break
    except:
        microDustData = 0.0
        microDustCount = 0
    
        
# print(microDustCount)
microDustData /= microDustCount
print(microDustData)
