import re

class InvalidRequestException(Exception):
    pass

class Request():
    def __init__(self, request):
        self.__raw_request = request
        self.__method = None
        self.__path = None
        self.__params = None
        self.__payload = None
        self.__parse()

    @property
    def key(self):
        return self.__path + self.__method
    
    @property
    def args(self):
        if self.__params:
            values = [v.split('=') for v in self.__params[1:].split('&')]
            return {v[0]: unquote(v[1]).decode('utf-8') for v in values}
        return {}

    @property
    def payload(self):
        return self.__payload

    def __parse(self):
        try:
            parts = self.__raw_request.split("\r\n")
            print(f'[parts={parts}]')
            if len(parts) < 1 and len(parts[0].split(' ')) != 3:
                raise InvalidRequestException('Request doesn\'t have the required minimum number of parts')
            m = re.search('(^[A-Z]+)\\s+(/[-a-zA-Z0-9_./=]+)(\?[-a-zA-Z0-9_.=&%]*)?', parts[0])
            self.__method, self.__path, self.__params = m.group(1), m.group(2), m.group(3) 
            print(f'[params={self.__params}]')
            if self.__method == 'POST':
                self.__payload = parts[7] 
        except Exception as e:
            raise InvalidRequestException(f'Request parse failed with Error: {str(e)}')

_hexdig = '0123456789ABCDEFabcdef'
_hextobyte = None

def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hextobyte

    if not string:
        return b''

    if isinstance(string, str):
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    if _hextobyte is None:
        _hextobyte = {(a + b).encode(): bytes([int(a + b, 16)])
                      for a in _hexdig for b in _hexdig}

    for item in bits[1:]:
        try:
            append(_hextobyte[item[:2]])
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)