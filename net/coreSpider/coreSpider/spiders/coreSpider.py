#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.conf import settings
from scrapy.log import start


import os
import sys
import getForms
import re

from scanner.mod_xss import Attack_XSS
from scanner.mod_permanentxss import Attack_permanentXSS
from net.HTTP import HTTP
import httplib2
import BeautifulSoup
###################
# 主爬虫类
###################

class coreSpider(BaseSpider):
    name = "coreSpider"
    allowed_domains = ["testfire.net"]
    start_urls = ["http://demo.testfire.net/"]
#    rules = (
#        Rule(SgmlLinkExtractor(allow=( ), deny=('\.jpg','\.pdf' ,'\.doc'))),
#    )

    g_url = []
    g_url_200 = []
    g_url_404 = []
    g_url_other = []
    g_forms = []
    g_getinfo = {}
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    link_encoding = {}
    
    def get_urls(self):
        return self.g_url_200
        
    def get_getinfo(self):
        
        return self.g_getinfo
    
    def get_forms(self, urls):
        
        return getForms.reForms(urls)
#        print '________________'
#        for u in urls:
#            print '****'
#            print u
#            print '*****'
#            f = getForms.crawlForm(u)
#            print '----------'
#            print self.g_forms
#            print '-----------'
#            if len(f) is not 0:
#                #print f
#                self.g_forms.append(f)
#        
#        #print f
#        
#        return self.g_forms
        
    
    def dealUrl(self, url, code):
        self.g_url.append(url)
        if code == 200:
            self.g_url_200.append(url)
            info, data = self.h.request(url)
            page_encoding = BeautifulSoup.BeautifulSoup(data).originalEncoding
            self.link_encoding[url] = page_encoding
            headers = info
            if headers != {}:
                if not headers.has_key("link_encoding"):
                    if self.link_encoding.has_key(url):
                        headers["link_encoding"] = self.link_encoding[url]
                
            #print headers
            self.g_getinfo[url] = headers
        elif code == 404:
            self.g_url_404.append(url)
        else:
            self.g_url_other.append(url)

    def getURL(self, html):
        print '%%%%%%%%%%%%%'
        urls=[]
        #print html
        if html:
            print '!!!!!!!!'
            soup = BeautifulSoup.BeautifulSoup(html)
            content=soup.findAll('a')
            print content
            for i in content:
                url=i["href"]
                print url
                if url and url[0:4]=="http":
                    urls.append(url)
                if url and url[0:4]!="http":
                    print url
        return urls  
     
    def getHyperLinks(self, baseUrl, data):
        links = []
        soup=BeautifulSoup.BeautifulSoup(data)
        a=soup.findAll("a",{"href":re.compile(".*")})
        for i in a:
            if i["href"].find("http://")!=-1:
                links.append(i["href"])
            else:
                links.append(baseUrl + i["href"])
        return links
    
    def parse(self, response):
        #print response.headers
        print '&&&&&&&&&&&&&&'
        print response.url
        self.dealUrl(response.url, response.status)
        
        hxs = HtmlXPathSelector(response)
#        base_url = hxs.select("//base/@href").extract()
#        print '-------'
#        print base_url
#        print '-------'
#        if 'testfire.net' in response.url:
#            soup = BeautifulSoup(response.body)
#            items = [(x[0].text, x[0].get('href')) for x in
#                    filter(None, [
#                    x.findChildren() for x in
#                    soup.findAll('td', {'class':'title'})
#                    ])]
        uuu = response.url
        urls =  self.getHyperLinks(uuu, response.body) 
        #urls = hxs.select('//a[contains(@href, "")]/@href').extract()
        
        for url in urls:
            if  url not in self.g_url:

                yield Request(url, callback=self.parse)         

        print len(self.g_url_200)
            

    def start_requests(self):
        print 'start request'
        if self.start_urls:
            h = {'User-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}
            
            return [Request(r, headers=h) for r in self.start_urls]


                    

def setting():
    #from scrapy.conf import settings
    #print settings['LOG_ENABLED']
    settings.overrides['BOT_NAME'] = 'coreSpider'
    settings.overrides['BOT_VERSION'] = '1.0'
    settings.overrides['DEPTH_LIMIT'] = 1
    settings.overrides['DOWNLOADER_DEBUG'] = True
    #settings.overrides['LOG_ENABLED'] = True
#    settings.overrides['LOG_LEVEL'] = 'DEBUG'
#    settings.overrides['LOG_STDOUT'] = False
#    settings.overrides['LOG_FILE'] = 'log.txt'
    ####for proxy
#    settings.overrides['DOWNLOADER_MIDDLEWARES'] = {
#    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#    'net.coreSpider.coreSpider.spiders.Mymiddlewares.ProxyMiddleware': 100,
#    }

#def setDir():
#    oDir = os.getcwd()
#    #os.system("cd ../..")
#    os.chdir("../..")
#    cmd = "scrapy crawl coreSpider"
#    #os.chdir("../.")
#    os.system(cmd)
#    print os.getcwd()
    
#def main_cmd():
#    setDir()
#    print '********************'
#    c = coreSpider()
#    getinfo = c.get_getinfo()
#    print getinfo
#    print c.get_urls()
#    forms = c.get_forms(c.get_urls()) 
#    print forms
#    print len(c.get_urls())
#    print "ENGINE STOPPED"
#    # scanner
#    h = HTTP()
#    a = Attack_XSS(h)
#    a.attack(getinfo,forms)
#    print '%%%%%%%%%%%%%%%'
    

def main_spider():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    def catch_item(sender, item, **kwargs):
        print "Got:", item

    dispatcher.connect(catch_item, signal=signals.item_passed)

    # setting
    setting()
    
    # set log
    start(logfile = 'l',loglevel = 'DEBUG',logstdout = False)
    # set up crawler
    from scrapy.crawler import CrawlerProcess

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(coreSpider())

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print '********************'
    c = coreSpider()
    getinfo = c.get_getinfo()
    print getinfo
    urls = c.get_urls()
    forms = c.get_forms(urls) 
    print forms
    print len(c.get_urls())
    print "ENGINE STOPPED"
    # scanner
    h = HTTP()
    a = Attack_XSS(h)
    tmp = a.attack(getinfo,forms)
    print '%%%%%%%%%%%%%%%'
    
    print 'per XSS start'
    
    p_xss = Attack_permanentXSS(h)
    p_xss.attack_p(getinfo, forms, tmp)
    
    

if __name__ == '__main__':
    main_spider()

#    
        