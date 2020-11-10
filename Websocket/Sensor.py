import RPi.GPIO as g
import board
import adafruit_dht as DHT
import time


# dht_device = DHT.DHT11(board.SCLK)
g.setmode(g.BCM)
g.setup(6, g.OUT)
g.setup(13, g.OUT)
g.output(6, True)
g.output(13, False)
time.sleep(10)

# g.setup(16, g.OUT)
# g.setup(20, g.OUT)
# g.setup(21, g.OUT)
# g.output(16, True)
# time.sleep(1)
# g.output(16, False)
# g.output(20, True)
# time.sleep(1)
# g.output(20, False)
# g.output(21, True)
# time.sleep(1)
# g.output(21, False)
g.cleanup()

# while True:
# print(dht_device.temperature * (9/5) + 32)
# print(dht_device.humidity)
# dht_device.exit()
#     time.sleep(5)
