

class NoidException(Exception):
    pass

class HTTPException(NoidException):  
    code = 0
    msg = None
    page = None
    def __init__(self, value=None):
        self.value = value
    def __str__(self):
        return str(self.code) + " " + str(self.msg)