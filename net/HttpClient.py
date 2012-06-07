#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

class HTTPResponse():
    data = ""
    code = "200"
    headers = {}
    def __init__(self, data, code, headers):
        self.data = data
        self.code = code
        self.headers = headers
    def getPage(self):
        "Return the content of the page."
        return self.data

    def getCode(self):
        "Return the HTTP Response code ."
        return self.code
    def getInfo(self):
        "Return the HTTP headers of the Response."
        return self.headers

    def getPageCode(self):
        "Return a tuple of the content and the HTTP Response code."
        return (self.data, self.code)

class HttpClient():
    def __init__(self):
        pass
    
    def send(self, target, post_data = None, http_params = {}, http_headers = {}, method=""):
        if post_data == None:
            if method == "get":
                self.req = requests.get(target, params=http_params, headers=http_headers)
                
                
        return HTTPResponse(self.req.text, self.req.status_code, self.req.headers)
        
if __name__ == "__main__":
    h = HttpClient()
    url = 'http://www.renren.com/'
    print h.send(url, method='get').getCode()
    #print h.send(url, method='get').getPage()
    print h.send(url, method='get').getInfo()    
    
            
        
        
