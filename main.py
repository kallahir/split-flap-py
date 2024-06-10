import gc
import time
import uasyncio
import ujson as json
import usocket as socket

from asyncserver.request import Request
from asyncserver.response import Response
from asyncserver.server import AsyncServer
from motor.stepper import StepperMotor 
from sensor.halleffect import HallEffect
from unit.unit import Unit
from unit.manager import UnitManager
from utils.http import HTML_CONTENT_TYPE, JSON_CONTENT_TYPE
from machine import Pin

print('[starting]')
tm = tm1637.TM1637(clk=Pin(23), dio=Pin(22))
tm.scroll('starting', delay=250)

# NOTE: Broadcast testing 
# config_file = open('config.json', 'r') 
# config = json.loads(config_file.read())
# print(f'group_id={config["group_id"]}')

# if config['group_id'] == 1:
#     while True:
#         print('broadcasting message')
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.sendto("leader", ('192.168.8.255', 1926))
#         time.sleep(5)
# else:
#     while True:
#         print('waiting broadcast')
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.bind(('192.168.8.255', 1926))
#         while True:
#             msg, addr = s.recvfrom(1024)
#             print(msg, addr)

# NOTE: Third wave of tests using Two Units in a single Unit Manager with fast interleave steps and no APIs
# units =[Unit(StepperMotor(32,33,25,26), 0, HallEffect(39)),Unit(StepperMotor(27,14,12,13), 1, HallEffect(36)),Unit(StepperMotor(15,2,0,4), 2, HallEffect(34))] 
# um = UnitManager(units)
# um.reset_units()
# time.sleep(1)
# um.move_to_letters('oi?')
# time.sleep(1)
# um.move_to_letters('zzz')

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
server = AsyncServer()

@server.route('/index')
async def on(r: Request) -> Response:
    gc.collect()
    return Response(content_type=HTML_CONTENT_TYPE, uri='ui/webpages/index.html')

@server.route('/config')
async def on(r: Request) -> Response:
    gc.collect()
    return Response(content_type=HTML_CONTENT_TYPE, uri='ui/webpages/config.html')

@server.route('/move')
async def on(r: Request) -> Response:
    gc.collect()
    print(f'[move:args={r.args}]')
    return Response(content_type=JSON_CONTENT_TYPE, content=json.dumps(r.args))

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
#         um.move_to_letters(r.args['letter'])
#         return server.response(200, content=f'unit moved to letter=' + r.args['letter'])
#     return server.response(400, content='invalid request')

loop = uasyncio.get_event_loop()
loop.create_task(server.start())

try: 
    loop.run_forever()
except Exception as e:
    print(f'[exception {e}]')
except KeyboardInterrupt:
    print('[stopping]')
    loop.close()