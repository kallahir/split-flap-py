class Route:
    def __init__(self, path, method, handler):
        self.__path = path 
        self.__method = method
        self.__handler = handler

    @property
    def key(self):
        return self.__path + self.__method

    @property
    def handler(self): 
        return self.__handler
