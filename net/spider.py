#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HttpClient import HttpClient
from bs4 import BeautifulSoup



class Spider():
    def __init__(self, rooturl):
        self.rooturl = rooturl
        self.h = HttpClient()
    
    def gethtml(self):      
        return self.h.send(self.rooturl,method='get')
        
        

if __name__ == "__main__":
#    s = Spider('http://www.renren.com/')
#    
#    print s.gethtml()
    pass

        

