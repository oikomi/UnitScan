#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re
import socket
from bs4 import BeautifulSoup
from net.HttpClient import HttpClient
from net.HttpClient import HTTPResponse



class Xss():
    
    
    GET_XSS = {}
    POST_XSS = {}
    
    def __init__(self):
        self.http = HttpClient()
        
    
    def attack(self, urls, forms):
        for url, headers in urls.items():
            dictio = {}
            params = []
            page = url
            
            if url.find("?") >= 0:
                page = url.split('?')[0]
                query = url.split('?')[1]
                params = query.split('&')
                if query.find("=") >= 0:
                    for param in params:
                        dictio[param.split('=')[0]] = param.split('=')[1]
            
            self.aGet(page, dictio, headers)
    
    def aGet(self, page, dict, headers = {}):
        """This method performs the cross site scripting attack (XSS attack) with method GET"""
        print page
        print dict
        if dict == {}:         
            url = page + "?__XSS__"      
            code = "".join([random.choice("0123456789abcdefghjijklmnopqrstuvwxyz") for i in range(0,10)])
            url = page + "?" + code
            self.GET_XSS[code] = url
            
            data = self.http.send(url,method='get').getPage()
            print '----------------'
            #print data
            if data.find(code) >= 0:
                print 'get it'
                #payloads = self.generate_payloads(data, code)
                #if payloads != []:
                    #self.findXSS(page, {}, "", code, "", payloads, headers["link_encoding"])
        else:
            for k in dict.keys():
                err = ""
                tmp = dict.copy()
                tmp[k] = "__XSS__"
                url = page + "?" + self.http.encode(tmp, headers["link_encoding"])
                
                code = "".join([random.choice("0123456789abcdefghjijklmnopqrstuvwxyz") for i in range(0,10)])
                tmp[k] = code
                print tmp
                url = page + "?" + self.http.encode(tmp, headers["link_encoding"])
                self.GET_XSS[code] = url
                data = self.http.send(url,method='get').getPage()
                
                if data.find(code) >= 0:
                    print 'get it'
            
       
       
if __name__ == "__main__":
    u = {u'http://history.sysu.edu.cn/archive/index.php?cateid=1': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=1', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:06:55 GMT; path=/, lastvisit=0%091339654015%09%2Farchive%2Findex.php%3Fcateid%3D1; expires=Fri, 14-Jun-2013 06:06:55 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:06:55 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:06:55 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?online=yes': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?online=yes', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/, lastvisit=0%091339654034%09%2Farchive%2Findex.php%3Fonline%3Dyes; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/, online1=yes; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:14 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=9': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=9', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:07 GMT; path=/, lastvisit=0%091339654027%09%2Farchive%2Findex.php%3Fcateid%3D9; expires=Fri, 14-Jun-2013 06:07:07 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:07 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:07 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?online=no': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?online=no', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/, lastvisit=0%091339654038%09%2Farchive%2Findex.php%3Fonline%3Dno; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/, online1=no; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:18 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:06:53 GMT; path=/, lastvisit=0%091339654013%09%2Farchive%2Findex.php%3F; expires=Fri, 14-Jun-2013 06:06:53 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:06:53 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:06:53 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=10': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=10', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:04 GMT; path=/, lastvisit=0%091339654024%09%2Farchive%2Findex.php%3Fcateid%3D10; expires=Fri, 14-Jun-2013 06:07:04 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:04 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:04 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=11': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=11', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:02 GMT; path=/, lastvisit=0%091339654022%09%2Farchive%2Findex.php%3Fcateid%3D11; expires=Fri, 14-Jun-2013 06:07:02 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:02 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:02 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=57': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=57', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:06:58 GMT; path=/, lastvisit=0%091339654018%09%2Farchive%2Findex.php%3Fcateid%3D57; expires=Fri, 14-Jun-2013 06:06:58 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:06:58 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:06:58 GMT', 'content-type': 'text/html'}}

    x = Xss()
    x.attack(u,'jj') 
        
        