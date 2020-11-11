import board
import adafruit_dht as DHT
import time
import threading
# dht_device = DHT.DHT22(board.SCLK) #pin set -- board.~~~
# # dht_device = DHT.DHT22(board.MISO) #pin set -- board.~~~
# # dht_device = DHT.DHT22(board.MOSI) #pin set -- board.~~~
# 
# def get_DHT_data():
#     print(dht_device.temperature)
#     print(dht_device.humidity)
# 
# try:
#     get_DHT_data()
#     time.sleep(2)
#     get_DHT_data()
#     time.sleep(2)
#     get_DHT_data()
# except:
#     try:
#         print("boom1")
#         dht_device.exit()
#         print("boom2")
#         dht_device = DHT.DHT22(board.SCLK)
#         print("boom3")
#         get_DHT_data()
#         time.sleep(2)
#         get_DHT_data()
#         time.sleep(2)
#         get_DHT_data()
#     except:
#         print("fxxc");
#         dht_device.exit()
#         exit()
# 
# dht_device.exit()

dht_id = 0

# dht_device = DHT.DHT22(board.SCLK) #pin set -- board.~~~
# dht_device = DHT.DHT22(board.MISO) #pin set -- board.~~~
dht_device = DHT.DHT22(board.MOSI) #pin set -- board.~~~

def DHT_dataThread():
    threading.Timer(10.0, DHT_dataThread).start()
#     try:
    print({'temperature' : dht_device.temperature, 'humidity' : dht_device.humidity})
#     except:
#         print("DHT_dataThread is not connect")
#         dht_device.exit()
#         exit()
def get_DHT_data():
    try:
        return {'temperature' : dht_device.temperature, 'humidity' : dht_device.humidity}
    except:
        print("get_DHT_data is not connect")
        dht_device.exit()
        exit()
        
while True:
    time.sleep(5)
    print({'temperature' : dht_device.temperature, 'humidity' : dht_device.humidity})
        
