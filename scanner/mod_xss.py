#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re
from bs4 import BeautifulSoup
from net.HttpClient import HttpClient
from net.HttpClient import HTTPResponse
from payloads.GetPayloads import loadPayloads

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
        self.independant_payloads = loadPayloads(self.CONFIG_DIR + "/" + self.CONFIG_FILE)
    
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
                    self.findXSS(page, {}, "", code, "", payloads, headers["link_encoding"])
                    
                    
                    
    
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
        soup = BeautifulSoup.BeautifulSoup(data)
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
                    
                    
                    
                    
        
                    
                    
                    