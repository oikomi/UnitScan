#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Python PycURL 网络编程

    在使用urllib的时候经常会死掉，以前debug过，是没有设置 timing out 所以超时后就会死掉。

    PycURL是curl的python库，虽然有些curl的功能没有实现，但是还是很强劲的。

    curl是非常强劲的一个工具，

    google内部用它来 debug GDATA API. Using cURL to interact with Google data services

    可以去 http://pycurl.sourceforge.net/ 下载最新的PycURL。
    简单的PycURL例子

    import pycurl
    import StringIO
     
    url = "http://www.google.com/"
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE,1)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.perform()
    print crl.fp.getvalue()

    PycURL 自动处理cookie

    import pycurl
    import StringIO
     
    url = "http://www.google.com/"
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE,1)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
     
    # Option -b/--cookie <name=string/file> Cookie string or file to read cookies from
    # Note: must be a string, not a file object.
    crl.setopt(pycurl.COOKIEFILE, "cookie_file_name")
     
    # Option -c/--cookie-jar <file> Write cookies to this file after operation
    # Note: must be a string, not a file object.
    crl.setopt(pycurl.COOKIEJAR, "cookie_file_name")
     
    crl.perform()
    print crl.fp.getvalue()

    PycURL 实现POST方法

    import pycurl
    import StringIO
    import urllib
     
    url = "http://www.google.com/"
    post_data_dic = {"name":"value"}
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE,1)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    #crl.setopt(pycurl.AUTOREFERER,1)
     
    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    #crl.setopt(pycurl.PROXY,proxy)
    crl.setopt(pycurl.HTTPPROXYTUNNEL,1)
    #crl.setopt(pycurl.NOSIGNAL, 1)
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.USERAGENT, "dhgu hoho")
     
    # Option -d/--data <data>   HTTP POST data
    crl.setopt(crl.POSTFIELDS,  urllib.urlencode(post_data_dic))
     
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.perform()
     
    print crl.fp.getvalue()

    urllib 超时设置

    import socket
    socket.setdefaulttimeout(5.0)
'''


import pycurl
import StringIO
import re
from bs4 import BeautifulSoup

def getURLContent_pycurl(url):
    c = pycurl.Curl()
    c.setopt(pycurl.URL,url)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)

    #c.setopt(pycurl.PROXY, 'http://11.11.11.11:8080')
    #c.setopt(pycurl.PROXYUSERPWD, 'aaa:aaa')
    c.perform()
    return b.getvalue()

def getHyperLinks(url):
    links=[]
    data=getURLContent_pycurl(url)
  
    soup=BeautifulSoup(data)
    a=soup.findAll("a",{"href":re.compile(".*")})
    for i in a:
        if i["href"].find("http://")!=-1:
            links.append(i["href"]) 
    return links

url = 'http://www.huawei.com/cn/'
content =getURLContent_pycurl(url)
print getHyperLinks('http://www.huawei.com/cn/')

