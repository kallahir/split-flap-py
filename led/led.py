import uasyncio

from machine import Pin
from utils.pin import PinNum

class Led:
    def __init__(self, pin_num=PinNum.D4):
        self.__led_pin = Pin(pin_num, Pin.OUT)
        self.__blink = False 
    
    def on(self):
        self.__led_pin.off()

    def off(self):
        self.__led_pin.on()
    
    async def blink(self):
        if self.__blink:
            self.off()
            await uasyncio.sleep(0.2)
            self.on()
            await uasyncio.sleep(0.2)
    
    def start_blink(self):
        self.__blink = True

    def stop_blink(self):
        self.__blink = False
