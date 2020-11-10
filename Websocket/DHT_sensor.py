import board
import adafruit_dht as DHT


dht_device = DHT.DHT11(board.SCLK) #pin set -- board.~~~

def get_DHT_data():
    print(dht_device.temperature * (9/5) + 32)
    print(dht_device.humidity)

dht_device.exit()