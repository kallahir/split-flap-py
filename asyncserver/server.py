import uasyncio

from asyncserver.request import Request
from asyncserver.response import Response
from asyncserver.route import Route
from utils.http import HTTP_CODES, HTML_CONTENT_TYPE

class AsyncServer(object):
    def __init__(self, host='0.0.0.0', port=80, buffer_length=4096):
        self.__host = host
        self.__port = port
        self.__buffer_length = buffer_length
        self.__routes = {}
        self.__writer = None
    
    def start(self):
        return uasyncio.start_server(self.__run, self.__host, self.__port)

    def route(self, path, method='GET'):
        def decorator(handler):
            r = Route(path, method, handler)
            if r.key in self.__routes:
                raise Exception(f'Path [{path}] already bound to Method [{method}]')
            self.__routes[r.key] = r
        return decorator

    async def __run(self, reader, writer):
        try:
            input = await reader.read(self.__buffer_length)
            request = Request(str(input, 'utf8')) 

            if request.key not in self.__routes:
                await self.__respond(Response(status_code=404, content='Route not found'))
            else:
                handler = self.__routes[request.key].handler
                response = await handler(request)
                await self.__respond(writer, response)
        except Exception as e:
            await self.__respond(writer, Response(status_code=500, content=f'Error: {str(e)}'))

        writer.close()
        await writer.wait_closed()

    async def __respond(self, writer, response: Response):
        if response.content_type == HTML_CONTENT_TYPE:
            await self.__serve_html(writer, response.uri) 
        else:
            await writer.awrite(bytes(f'HTTP/1.1 {response.status_code} {HTTP_CODES[response.status_code]}\r\nContent-Type: {response.content_type}\r\n\r\n{response.content}', 'utf8'))
    
    async def __serve_html(self, writer, uri: str):
        try:
            with open(uri) as html_file:
                writer.write('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'.encode('utf-8'))
                chunk = html_file.read(self.__buffer_length)
                while chunk:
                    writer.write(chunk.encode('utf-8'))
                    await writer.drain()
                    chunk = html_file.read(self.__buffer_length)
        except FileNotFoundError:
            await self.__respond(writer, Response(status=404, content='File not found'))
