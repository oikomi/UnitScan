#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

class HttpClient():
    def __init__(self):
        pass
    
    def send(self, target, post_data = None, http_params = {}, http_headers = {}, method=""):
        if post_data == None:
            if method == "get":
                self.req = requests.get(target, params=http_params, headers=http_headers)
                
                
        return self.req.text
        

            
        
        
