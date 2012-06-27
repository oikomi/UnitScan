#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
http://blog.csdn.net/cashey1991/article/details/6262704
'''

import WebCrawler  
  
url = 'http://www.baidu.com/'
thNumber = 5
Maxdepth = 2
  
wc = WebCrawler.WebCrawler(thNumber, Maxdepth)  
wc.Craw(url)  

print WebCrawler.getUrl()

print '**********************'