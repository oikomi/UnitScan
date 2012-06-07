#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re
from net.HttpClient import HttpClient
from net.HttpClient import HTTPResponse

class mod_xss():
    """
    This class implements a cross site scripting attack
    """
    def __init__(self):
        
        self.allowed = ['php', 'html', 'htm', 'xml', 'xhtml', 'xht', 'xhtm',
              'asp', 'aspx', 'php3', 'php4', 'php5', 'txt', 'shtm',
              'shtml', 'phtm', 'phtml', 'jhtml', 'pl', 'jsp', 'cfm',
              'cfml', 'py']
        self.http = HttpClient()
    
    def attackGET(self, page, dict, headers = {}):
        """This method performs the cross site scripting attack (XSS attack) with method GET"""
        if dict == {}:
            if not headers.has_key("content-type"):
                if (page.split(".")[-1] not in self.allowed) and page[-1] != "/":
                    return
            elif headers["content-type"].find("text") == -1:
                return
            
            url = page + "?__XSS__"      
            code = "".join([random.choice("0123456789abcdefghjijklmnopqrstuvwxyz") for i in range(0,10)])
            url = page + "?" + code
            data = self.http.send(url).getPage()
            if data.find(code) >= 0:
                payloads = self.generate_payloads(data, code)
                if payloads != []:
            
            
            
            
        
      