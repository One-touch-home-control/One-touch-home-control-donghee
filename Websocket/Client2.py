import socketio
import RPi.GPIO as g
import Adafruit_DHT



sensor = Adafruit_DHT.DHT11
io = socketio.Client()


LED_PIN = [16, 20, 21]


#let rooms = []
#let leds = []
#let dust = 0
#let neoPixel = {
#    r: 0,
#    g: 0,
#    b: 0,
#    status: false
#}
#let waterStatus = {
#    status: false
#}
#let powerwall = {
#    status: false,
#    current: 0
#}

g.setmode(g.BCM)
g.setup(LED_PIN[0], g.OUT)
g.setup(LED_PIN[1], g.OUT)
g.setup(LED_PIN[2], g.OUT)

class Room:
    def __init__(self, id = -1, address ="Undefined"):
        self.id = id
        self.address = address
    def toJSON(self):
        return {'id': self.id, 'address': self.address}
class Led:
    def __init__(self, id = -1, status = False):
        self.id = id
        self.status = status
    def toJSON(self):
        return {'id': self.id, 'status': self.status}

class Dth:
    def __init__(self, id = -1, temp = 0, humi = 0):
        self.id = id
        self.temp = temp
        self.humi = humi
    def toJSON(self):
        return {'id': self.id, 'temp': self.temp, 'humi': self.humi}
class NeoPixel:
    def __init__(self, r = 0, g = 0, b = 0, status = False):
        self.r = r
        self.g = g
        self.b = b
        self.status = status
    def toJSON(self):
        return {
            'r': self.r,
            'g': self.g,
            'b': self.b,
            'status': self.status
        }
class PowerWall:
    def __init__(self, status = False, current = 0):
        self.status = status
        self.current = current
    def toJSON(self):
        return {
           'status': self.status,
           'current': self.current
       }
rooms = []
leds = []
dths = []
neopixels = NeoPixel()
dusts = 0
waterStatus = False
powerWall = PowerWall()

@io.event
def connect():
    print("Conenct is success!")
    io.emit('change', 'arduino')
@io.event
def init(data):
    global dusts
    print("Init is called!")
    print(data)
    if 'id' in data:
        #If is request from android we should send current data.
        #led, dust, neopixel, waterstatus, powerwall
        ledObj = []
        dthObj = []
        for value in leds:
            ledObj.append(value.toJSON())
        for value in dths:
            dthObj.append(value.toJSON()) 
        io.emit('init', {
            'id': data['id'],
            'led': ledObj,
            'dth': dthObj,
            'dust': dusts,
            'neoPixel': neopixels.toJSON(),
            'waterStatus': waterStatus,
            'powerwall': powerWall.toJSON()
        })
    else:
        rooms.clear()
        
        print(g.input(LED_PIN[0]))
        print(g.input(LED_PIN[1]))
        print(g.input(LED_PIN[2]))
        
        for value in data['roomList']:
            rooms.append(Room(value['id'], value['name']))
        leds.clear()
        dths.clear()
        for value in rooms:
            leds.append(Led(value.id, g.input(LED_PIN[value.id - 1]) == True))
            dths.append(Dth(value.id, 24.2, 45))
        dusts = 20
        ledObj = []
        dthObj = []
        for value in leds:
            ledObj.append(value.toJSON())
        for value in dths:
            dthObj.append(value.toJSON()) 
        io.emit('init', {
            'led': ledObj,
            'dth': dthObj,
            'dust': dusts,
            'neoPixel': neopixels.toJSON(),
            'waterStatus': waterStatus,
            'powerwall': powerWall.toJSON()
        })
    print('id' in data)
@io.event
def led(data):
    if data['room'] == 0:
        print("input zero!!")
        all_led_off = True
        for pin in LED_PIN:
            if g.input(pin) == True:
                all_led_off = False
        for pin in LED_PIN:
            g.output(pin, all_led_off)
    for led in leds:
        if led.id == data['room']:
            led.status = data['status']
            io.emit('led', data)
            g.output(LED_PIN[led.id - 1], led.status)
            for l in leds:
                print(l.toJSON())
@io.event
def add_room(data):
    print("Add room request")
    rooms.append(Room(data['id'], data['address']))
    leds.append(Led(data['id'], False))
    dths.append(Dth(data['id'], 24.2, 45))

@io.event
def neopixel(data):
    global neopixels
    print("Change neopixel before")
    print(neopixels.toJSON())
    neopixels = NeoPixel(data['r'], data['g'], data['b'], data['status'])
    print("END")
    print(neopixels.toJSON())
    
@io.event
def water_state(data):
    global waterStatus
    print("Request water change")
    waterStatus = data['status']
    io.emit('water_status', waterStatus)
    # pump on off
    
def updateDust(dust):
    global dusts
    dusts = dust
    io.emit('dust', dusts)
    
def updatePowerWall(data):
    powerWall.status = data['status']
    powerWall.current = data['current']
    io.emit('powerwall', powerWall.toJSON())
    
io.connect("http://192.168.10.190:8080")
io.wait()