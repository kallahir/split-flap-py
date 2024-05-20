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
            return {v[0]: v[1] for v in values}
        return {}

    def empty(self):
        return len(self.__raw_request) == 0
    
    def __parse(self):
        parts = self.__raw_request.split("\r\n")
        print(parts)
        if len(parts) < 1 and len(parts[0].split(' ')) != 3:
            raise InvalidRequestException()
        m = re.search('(^[A-Z]+)\\s+(/[-a-zA-Z0-9_./=]+)(\?[-a-zA-Z0-9_.=&]*)?', parts[0])
        self.__method, self.__path, self.__params = m.group(1), m.group(2), m.group(3) 
        print(f'[params={self.__params}]')
        if self.__method == 'POST':
            self.__payload = parts[7] 
