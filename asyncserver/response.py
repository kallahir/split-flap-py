from utils.http import HTML_CONTENT_TYPE

class InvalidResponseException(Exception):
    pass

class Response(object):
    def __init__(self, status_code=200, content_type='text/plain', uri=None, content=None):
        self.__status_code = status_code
        self.__content_type = content_type
        self.__uri = uri
        self.__content = content
        self.__validate()
    
    @property
    def status_code(self):
        return self.__status_code

    @property
    def content_type(self):
        return self.__content_type
    
    @property
    def uri(self):
        return self.__uri

    @property
    def content(self):
        return self.__content
    
    def __validate(self):
        if self.__content_type == HTML_CONTENT_TYPE and not self.__uri:
            raise InvalidResponseException('Response with Content-Type: text/html must have an URI')