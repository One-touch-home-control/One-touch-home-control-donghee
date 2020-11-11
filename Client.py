import socketio
import time
import RPi.GPIO as g

sio = socketio.Client()
led_is_on = 0

g.setmode(g.BCM)
g.setup(27, g.OUT)
@sio.event
def message(data):
    print('I received a message!')

@sio.on('message')
def on_message(data):
    print('I received a message!')

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('change', {'txt':'arduino'})
    
@sio.event
def disconnect():
    logger.info('disconnected from server')

@sio.event
def init(data):
    global led_is_on
    sio.emit('led', led_is_on)
    
@sio.event
def led(data):
    global led_is_on
    if(data['led'] == 1):
        g.output(27, True)
        led_is_on = 1
    else:
        g.output(27, False)
        led_is_on = 0

sio.connect('http://192.168.10.190:80')
g.cleanup()

sio.wait()

    