import RPi.GPIO as g
import time

g.setmode(g.BCM)
g.setup(16, g.OUT)
g.setup(20, g.OUT)
g.setup(21, g.OUT)
g.output(16, True)
time.sleep(1)
g.output(16, False)
g.output(20, True)
time.sleep(1)
g.output(20, False)
g.output(21, True)
time.sleep(1)
g.output(21, False)
g.cleanup()