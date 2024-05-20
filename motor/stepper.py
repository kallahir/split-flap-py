from machine import Pin
import time

FULL_ROTATION = 4096
SEQ = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

class Direction(object):
    FORWARD = 0
    BACKWARD = 0

class StepperMotor(object):
    def __init__(self, in1, in2, in3, in4):
        self.__in1 = Pin(in1, Pin.OUT)
        self.__in2 = Pin(in2, Pin.OUT)
        self.__in3 = Pin(in3, Pin.OUT)
        self.__in4 = Pin(in4, Pin.OUT)

    def move(self, distance, direction=Direction.FORWARD, delay=3):
        if distance == 0:
            return
        elif direction == Direction.FORWARD:
            for _ in range(0, distance):
                self.move_forward(delay)
        elif direction == Direction.BACKWARD:
            for _ in range(0, distance):
                self.move_backward(delay)
        time.sleep_ms(250)

    def move_forward(self, delay=3):
        for step in SEQ:
            self.__in1.value(step[0])
            self.__in2.value(step[1])
            self.__in3.value(step[2])
            self.__in4.value(step[3])
            time.sleep_ms(delay)

    def move_backward(self, delay=3):
        for step in reversed(SEQ):
            self.__in1.value(step[0])
            self.__in2.value(step[1])
            self.__in3.value(step[2])
            self.__in4.value(step[3])
            time.sleep_ms(delay)

    def stop(self, delay=3):
        self.__in1.value(0)
        self.__in2.value(0)
        self.__in3.value(0)
        self.__in4.value(0)
        time.sleep_ms(delay)
