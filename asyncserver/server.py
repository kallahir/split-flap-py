import re
import uasyncio

from asyncserver.request import Request
from asyncserver.route import Route
from utils.http import HTTP_CODES

class AsyncServer(object):
    def __init__(self, host='0.0.0.0', port=80, buffer_length=2056):
        self._host = host
        self._port = port
        self._buffer_length = buffer_length
        self._routes = {}
    
    def start(self):
        return uasyncio.start_server(self.__run, self._host, self._port)

    def route(self, path, method='GET'):
        def decorator(handler):
            r = Route(path, method, handler)
            if r.key in self._routes:
                raise Exception(f'path={path} already bound to method={method}')
            self._routes[r.key] = r
        return decorator

    async def __run(self, reader, writer):
        input = await reader.read(self._buffer_length)
        request = Request(str(input, 'utf8')) 
        if request.key in self._routes:
            print('[route found]')
            try:
                response = await self._routes[request.key].handler(request)
            except Exception as e:
                response = self.response(500, content={"error": str(e)})
        else:
            print('[no route found]')
            response = self.response(404)
        await writer.awrite(response)
        uasyncio.sleep(0.2)
        await writer.wait_closed()

    def response(self, http_status, content_type='application/json', content=None):
        return bytes(f'HTTP/1.1 {http_status} {HTTP_CODES[http_status]}\r\nContent-Type: {content_type}\r\n\r\n{content}', 'utf8')
