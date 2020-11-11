import RPi.GPIO as g

g.setmode(g.BCM)
g.setup(2, g.IN)
print("abc")