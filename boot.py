import network
import time

from led.led import Led

print('[booting]')

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

wifi_led = Led()
for _ in range(20):
    wifi_led.off()
    time.sleep(0.1)
    wifi_led.on()
