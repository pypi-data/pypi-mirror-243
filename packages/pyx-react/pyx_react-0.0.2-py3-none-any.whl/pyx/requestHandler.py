
import random

class RequestHandler:
    def __init__(self):
        self.handlers = {}
        self.requests = {}

    # Request data from client
    def request(self, data, callback):
        callbackID = hex(random.randint(0, 0xffffffff))[2:]
        self.requests[callbackID] = callback
        return {'data': data, 'callbackID': callbackID}

    def handleResponse(self, data):
        if data['callbackID'] in self.requests:
            self.requests[data['callbackID']](data['data'])
            del self.requests[data['callbackID']]

    def handleRequest(self, data):
        return self.handlers[data['name']](data['data']) if data['name'] in self.handlers else None
    
    def registerHandler(self, eventName, handler):
        self.handlers[eventName] = handler
