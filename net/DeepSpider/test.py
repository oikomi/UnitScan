#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
http://blog.csdn.net/cashey1991/article/details/6262704
'''

import WebCrawler  
  
url = 'http://history.sysu.edu.cn/archive/index.php'
thNumber = 10
Maxdepth = 2
  
wc = WebCrawler.WebCrawler(thNumber, Maxdepth)  
wc.Craw(url)  

print WebCrawler.getUrl()