import machine
import time
import uasyncio

from asyncserver.request import Request
from asyncserver.server import AsyncServer
from motor.stepper import StepperMotor 
from sensor.halleffect import HallEffect
from unit.unit import Unit
from unit.manager import UnitManager

print('[starting]')
# NOTE: Third wave of tests using Two Units in a single Unit Manager with fast interleave steps and no APIs
um = UnitManager([Unit(StepperMotor(32,33,25,26), 0, HallEffect(39)),Unit(StepperMotor(27,14,12,13), 1, HallEffect(36))])
um.reset_units()
um.move_to_letters('oi')
time.sleep(1)
um.move_to_letters('bl')

# NOTE: Second wave of tests using Two Units, one at a time, and no APIs
# m = StepperMotor(32,33,25,26)
# s = HallEffect(39)
# u = Unit(m, 0, s)

# m1 = StepperMotor(27,14,12,13)
# s1 = HallEffect(36)
# u1 = Unit(m1, 1, s1)

# while True:
#     u.reset()
#     time.sleep_ms(500)
#     u1.reset()
#     time.sleep(5)

# NOTE: First wave of tests using a Single Unit and Async APIs for control
# server = AsyncServer()

# @server.route('/index')
# async def on(r: Request):
#     page_content = open('/data/main.html', 'r').read()
#     return server.response(200, content_type='text/html', content=page_content)

# @server.route('/reset')
# async def on(r: Request):
#     u.reset()
#     return server.response(200, content='unit reset')

# @server.route('/reboot')
# async def on(r: Request):
#     machine.reset()

# @server.route('/move')
# async def on(r: Request):
#     print(f'[args={r.args}]')
#     if 'letter' in r.args:
#         u.move_to_letter(r.args['letter'])
#         return server.response(200, content=f'unit moved to letter=' + r.args['letter'])
#     return server.response(400, content='invalid request')

# loop = uasyncio.get_event_loop()
# loop.create_task(server.start())

# try: 
#     loop.run_forever()
# except Exception as e:
#     print(f'[exception {e}]')
# except KeyboardInterrupt:
#     print('[stopping]')
#     loop.close()