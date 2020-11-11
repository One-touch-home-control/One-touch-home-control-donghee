import time
from rpi_ws281x import *
import argparse
import time

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

# def theaterChase(strip, color, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     for j in range(iterations):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, color)
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)
# 
# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)
# 
# def rainbow(strip, wait_ms=20, iterations=1):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i+j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)
# 
# def rainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)
# 
# def theaterChaseRainbow(strip, wait_ms=50):
#     """Rainbow movie theater light style chaser animation."""
#     for j in range(256):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, wheel((i+j) % 255))
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    #args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration. 스트립 생성
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions). 스트립 시작
    strip.begin()

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            """
            a = 0;
            for i in range(0, strip.numPixels()):
                if(a == 0):
                    colorSetting(strip, Color(255,0,0), i)
                elif(a == 1):
                    colorSetting(strip, Color(0,255,0), i)
                elif(a == 2):
                    colorSetting(strip, Color(0,0,255), i)
                a+=1
                if(a == 3):
                    a=0
                    """
            
#             for i in range(0, strip.numPixels()):
            colorSetting(strip, Color(30,20,30))
            stripShow(strip)
            time.sleep(10)
            
            colorWipe(strip, Color(0,0,0), 0)
#            print ('Color wipe animations.')
#            colorWipe(strip, Color(255, 0, 0), 0)  # Red wipe
#            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#            colorWipe(strip, Color(0, 0, 255))  # Green wipe
#            print ('Theater chase animations.')
#            theaterChase(strip, Color(127, 127, 127))  # White theater chase
#            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#            print ('Rainbow animations.')
#            rainbow(strip)
#            rainbowCycle(strip)
#            theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 0)
        print('\n')