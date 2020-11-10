import socketio
import RPi.GPIO as g
import time
import serial

from rpi_ws281x import *
import argparse

io = socketio.Client()

#-----------------------------------------------------------------------------------
# LED strip configuration:
LED_COUNT      = 20      # Number of LED pixels. ￣led
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# strip 각자 색 지정 가능 기본설정은 한색으로 다 넣기
def colorSetting(strip, color, pin=-1):
    if(pin != -1):
        strip.setPixelColor(pin, color)
    else:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        
# strip 보여주기, 순차적으로 보여주기 형태로 딜레이 존재
def stripShow(strip):
    for i in range(strip.numPixels()):
        strip.show()


# Define functions which animate LEDs in various ways. strip.setPixelColor 에 넣을 핀번호와 색(color( , , ) rgb) 형태로 넣으면 설정, show 하면 보여줌
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions). 스트립 시작
strip.begin()
#-------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------
ser = serial.Serial('/dev/ttyACM1', 9600)

def getMicroDust():
    microDustData = 0.0
    microDustCount = 0
    while True:
        try:
            for i in range(10):
                while True:
                    if(ser.in_waiting >0):
                        line = ser.readline()
#                         print(line)
#                         print(len(line))
                        try:
                            readData = float(line)
                        except:
                            continue
#                         print(readData)
#                         print()
                        if readData > 10 and readData < 100:
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
            
#     print(microDustCount)
    microDustData /= microDustCount
    return microDustData
#---------------------------------------------------------------------

print(getMicroDust())
print(getMicroDust())
print(getMicroDust())
print(getMicroDust())
print(getMicroDust())
print(getMicroDust())
print(getMicroDust())
print(getMicroDust())
print(getMicroDust())
print(getMicroDust())



SERVO_PIN = 12

g.setmode(g.BCM)
g.setup(SERVO_PIN, g.OUT)
servoPWM = g.PWM(SERVO_PIN, 50)
servoPWM.start(7.5)

LED_PINS = [13,6,5,21,20,16]
ledPWM = []

g.setmode(g.BCM)
for idx, pin in enumerate(LED_PINS):
    g.setup(pin, g.OUT)
    ledPWM.append(g.PWM(pin, 100))
    ledPWM[idx].start(50)
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
class Room:
    def __init__(self, id = -1, address ="Undefined", inside = False, dust = 0, neopixel = 0, pump = 0, servo = 0, dth = 0, camera = 0, led =0):
        self.id = id
        self.address = address
        self.inside = inside
        self.dust = dust
        self.neopixel = neopixel
        self.pump = pump
        self.servo = servo
        self.dth = dth
        self.camera = camera
        self.led = led
    def toJSON(self):
        return {
        'id': self.id,
        'address': self.address,
        'inside' : self.inside,
        'dust' : self.dust,
        'neopixel' : self.neopixel,
        'pump' : self.pump,
        'servo' : self.servo,
        'dth' : self.dth,
        'camera': self.camera,
        'led' : self.led
        }
class Led:
    def __init__(self, id = -1, pwm = 0):
        self.id = id
        self.pwm = pwm
    def toJSON(self):
        return {'id': self.id, 'pwm': self.pwm}

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
dths = []
leds_dictionaries = {}
neopixels = NeoPixel()
dusts = 0
waterStatus = False
powerWall = PowerWall()
servoStatus = False
@io.event
def connect():
    print("Conenct is success!")
    io.emit('change', 'arduino')
@io.event
def init(data):
    global dusts, servoStatus
    print("Init is called!")
    print(data)
    if 'id' in data:
        #If is request from android we should send current data.
        #led, dust, neopixel, waterstatus, powerwall
        ledObj = []
        dthObj = []
        for value in leds_dictionaries:
            print(Led(int(value), leds_dictionaries[str(value)]).toJSON())
            ledObj.append(Led(int(value), leds_dictionaries[str(value)]).toJSON())
        print()
        print(ledObj)
        io.emit('init', {
            'id': data['id'],
            'led': ledObj,
        })
        for value in dths:
            dthObj.append(value.toJSON()) 
        io.emit('init', {
            'id': data['id'],
            'dth': dthObj,
        })
        io.emit('init', {
            'id': data['id'],
            'dust': int(getMicroDust()),
        })
        io.emit('init', {
            'id': data['id'],
            'neoPixel': neopixels.toJSON(),
        })
        io.emit('init', {
            'id': data['id'],
            'waterStatus': waterStatus,
        })
        io.emit('init', {
            'id' : data['id'],
            'servo': {'status' : servoStatus},
        })
        #io.emit('init', {
        #    'id': data['id'],
        #    'powerwall': powerWall.toJSON()
        #})
    else:
        rooms.clear()
        leds_dictionaries.clear()
        for value in data['roomList']:
            leds_dictionaries[str(value['id'])] = 50
            rooms.append(Room(value['id'], value['name'], value['inside'], value['dust'], value['neopixel'], value['pump'], value['servo'], value['dth'], value['camera'], value['led']))
        print("leds_dictionaries : " + str(leds_dictionaries))
        dths.clear()
        for value in rooms:
            dths.append(Dth(value.id, 24.2, 45))
        dusts = 20
        ledObj = []
        dthObj = []
        for value in leds_dictionaries:
            ledObj.append(Led(int(value), leds_dictionaries[str(value)]).toJSON())
        io.emit('init', {
            'led': ledObj,
        })
        for value in dths:
            dthObj.append(value.toJSON()) 
        io.emit('init', {
            'dth': dthObj,
        })
        io.emit('init', {
            'dust': int(getMicroDust()),
        })
        io.emit('init', {
            'neoPixel': neopixels.toJSON(),
        })
        io.emit('init', {
            'waterStatus': waterStatus,
        })
        io.emit('init', {
            'powerwall': powerWall.toJSON()
        })
        io.emit('init', {
            'servo': {'status' : servoStatus},
        })
    print('id' in data)
@io.event
def led(data):
    leds_dictionaries[str(data['room'])] = data['pwm']
#     print(data['room'])
    print(leds_dictionaries[str(data['room'])])
    
    
    io.emit('led', data)
    
    ledPWM[int(data['room']) - 3].ChangeDutyCycle(int(data['pwm']))
    
#     for led in leds:
#         if led.id == data['room']:
#             leds[leds.index(led)] = Led(data['room'], data['pwm'])
#             io.emit('led', data)
@io.event
def add_room(data):
    print("Add room request")
    rooms.append(Room(data['id'], data['address'], data['inside'], data['dust'], data['neopixel'], data['pump'], data['servo'], data['dth'], data['camera'], data['led']))
    leds.append(Led(data['id'], 50))
    dths.append(Dth(data['id'], 24.2, 45))

@io.event
def neopixel(data):
    global neopixels
    print("Change neopixel before")
    print(neopixels.toJSON())
    neopixels = NeoPixel(data['r'], data['g'], data['b'], data['status'])
    if(data['status'] == True):
        colorSetting(strip, Color(data['r'],data['g'],data['b']))
        stripShow(strip)
    else:
        colorWipe(strip, Color(0,0,0), 0)
    print("END")
    print(neopixels.toJSON())
@io.event
def water_state(data):
    global waterStatus
    print("Request water change")
    waterStatus = data['status']
    io.emit('water_state', {'status': waterStatus})
@io.event
def servo(data):
    global servoStatus
    if(servoStatus == data['status']):
        return
    print("Request servo change")
    servoStatus = data['status']
    if servoStatus == True:
        servoPWM.ChangeDutyCycle(12)
    else:
        servoPWM.ChangeDutyCycle(7.5)
    io.emit('servo', {'status': servoStatus})
    print(servoStatus)
@io.event
def add_sensor(data):
    global dusts, neopixels, waterStatus
    roomInfo = data['room']
    sensorInfo = data['updated']
    print("Sensor update!")
    for roomValue in rooms:
        if roomValue.id ==roomInfo['id']:
            roomValue = Room(roomInfo['id'], roomInfo['name'], roomInfo['inside'], roomInfo['dust'], roomInfo['neopixel'], roomInfo['pump'], roomInfo['servo'], roomInfo['dth'], roomInfo['camera'], roomInfo['led'])
    if sensorInfo['sensor'] == 'dust':
        dusts = sensorInfo['initvalue']
    if sensorInfo['sensor'] == 'neopixel':
        neopixels = NeoPixel(sensorInfo['initvalue']['r'], sensorInfo['initvalue']['g'], sensorInfo['initvalue']['b'], sensorInfo['initvalue']['status'])
    if sensorInfo['sensor'] == 'pump':
        waterStatus = sensorInfo['initvalue']
    if sensorInfo['sensor'] == 'servo':
        pass
    if sensorInfo['sensor'] == 'dth':
        dths.append(Dth(sensorInfo['initvalue']['id'], sensorInfo['initvalue']['temp'], sensorInfo['initvalue']['humi']))
    if sensorInfo['sensor'] == 'camera':
        pass
    if sensorInfo['sensor'] == 'led':
        leds.append(Led(sensorInfo['initvalue']['id'], sensorInfo['initvalue']['pwm']))
    print("Sensor is Updated!")
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

