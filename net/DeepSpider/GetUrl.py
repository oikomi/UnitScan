#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


urlSep = ['<','>','//','(',')', r'"', r"'", ' ', '\t', '\n']
urlTag = ['http://']

def is_sep(ch):
    for c in urlSep:
        if c == ch:
            return True
    return False

def find_first_sep(i,s):
    while i < len(s):
        if is_sep(s[i]):
            return i
        i+=1
    return len(s)

def GetUrl(strPage):
    rtList = []
    for tag in urlTag:
        i = 0
        i = strPage.find(tag, i, len(strPage))
        while i != -1:
            begin = i
            end = find_first_sep(begin+len(tag),strPage)
            rtList.append(strPage[begin:end])
            i = strPage.find(tag, end, len(strPage))

    return rtList

def getHyperLinks(data):
    links = []
    soup=BeautifulSoup(data)
    a=soup.findAll("a",{"href":re.compile(".*")})
    #print a
    for i in a:
        if i["href"].find("http://")!=-1:
            links.append(i["href"]) 
    return links

