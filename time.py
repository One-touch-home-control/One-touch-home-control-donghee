import time
import GS_timing as timing

def delayMicroseconds(n):
    time.sleep(n / 1000000.)

def delayMillisecond(n):
    time.sleep(n / 1000.)

t_start = 0
t_end = 0

#using time.sleep
print('using time.sleep')
print('delayMicroseconds(1)')
for x in range(10):
    t_start = timing.micros() #us 
    delayMicroseconds(1)
    t_end = timing.micros() #us
    print('dt (us) = ' + str(t_end - t_start))
print('delayMicroseconds(2000)')
for x in range(10):
    t_start = timing.micros() #us 
    delayMicroseconds(2000)
    t_end = timing.micros() #us
    print('dt (us) = ' + str(t_end - t_start))
  
#using GS_timing
print('\nusing GS_timing')
print('timing.delayMicroseconds(1)')
for x in range(10):
    t_start = timing.micros() #us 
    timing.delayMicroseconds(1)
    t_end = timing.micros() #us
    print('dt (us) = ' + str(t_end - t_start))
print('timing.delayMicroseconds(2000)')
for x in range(10):
    t_start = timing.micros() #us 
    timing.delayMicroseconds(2000)
    t_end = timing.micros() #us
    print('dt (us) = ' + str(t_end - t_start))

# from datetime import datetime
# 
# dt = datetime.now()
# current = dt.microsecond
# time.sleep(1)
# dt = datetime.now()
# current2 = dt.microsecond
# print(current2 - current)
# current = time.time()*1000000
# time.sleep(0.0001)
# current2 = time.time()*1000000
# print(current2 - current)
# print(time.time() * 1000)