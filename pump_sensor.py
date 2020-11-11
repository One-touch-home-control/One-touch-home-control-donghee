import RPi.GPIO as g

pump_pin1 = 6  #pin set
pump_pin2 = 13 #pin set

g.setmode(g.BCM)
g.setup(pump_pin1, g.OUT)
g.setup(pump_pin2, g.OUT)

def pump_start():
    g.output(pump_pin1, True)
    g.output(pump_pin2, False)
    
def pump_stop():
    g.output(pump_pin1, False)
    g.output(pump_pin2, False)


g.cleanup()