import network
import time
import tm1637
from machine import Pin

print('[booting]')
tm = tm1637.TM1637(clk=Pin(23), dio=Pin(22))
tm.scroll('booting', delay=250)

secrets = open('secrets.txt', 'r').read()
ssid, password = secrets.split(',')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if not wlan.isconnected():
    raise RuntimeError('network connection failed')
else:
    print('connected')
    details = wlan.ifconfig()
    print('ip = ' + details[0])
    print(f'details {details}')
