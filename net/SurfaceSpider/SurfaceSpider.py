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

class SurfaceSpider():
    def __init__(self):
        self.c = pycurl.Curl()
        self.b = StringIO.StringIO()
        self.links=[]
    
    def getInfo(self,url):
        crl = pycurl.Curl()
        crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.FOLLOWLOCATION, 1)
        crl.setopt(pycurl.MAXREDIRS, 5)
        crl.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
        crl.fp = StringIO.StringIO()
        crl.setopt(pycurl.URL, url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        crl.perform()
        return crl.getinfo(pycurl.HTTP_CODE)
        
        
        
    def getContent(self,url):
        self.c.setopt(pycurl.URL,url)
        self.c.setopt(pycurl.WRITEFUNCTION, self.b.write)
        self.c.setopt(pycurl.MAXREDIRS, 5) 
        self.c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
        self.c.perform()
        return self.b.getvalue()
        
    def getHyperLinks(self,url):
        
        data=self.getContent(url)
  
        soup=BeautifulSoup(data)
        a=soup.findAll("a",{"href":re.compile(".*")})
        print a
        for i in a:
            if i["href"].find("http://")!=-1:
                self.links.append(i["href"]) 
        return self.links
    
    #def 
    
    #def getForms(self,url):
        

url = 'http://www.huawei.com/cn/'
ss = SurfaceSpider()
#content =ss.getContent(url)
#print ss.getHyperLinks('http://www.huawei.com/cn/')
#print ss.getInfo('http://www.huawei.com/cn/')
for a in ss.getHyperLinks('http://history.sysu.edu.cn/archive/index.php'):
    print a
    #print ss.getInfo(url)
    #print a

