from machine import Pin

class HallEffect(object):
    def __init__(self, pin):
        self.__sensor = Pin(pin, Pin.IN)
    
    def get_value(self):
        return self.__sensor.value() 
