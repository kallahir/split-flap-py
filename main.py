from motor.stepper import StepperMotor 
from sensor.halleffect import HallEffect
from unit.unit import Unit

m = StepperMotor(32,33,25,26)
s = HallEffect(13)
u = Unit(m, 0, s)

u.reset()
while True:
    letter = input('letter: ')
    u.move_to_letter(letter)