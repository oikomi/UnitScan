'''
http://zoulc001.iteye.com/blog/1186996

'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import socket
import urllib2
import re

class MyCrawler:
    def __init__(self,seeds):
        self.linkQuence=linkQuence()
        if isinstance(seeds,str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds,list):
            for i in seeds:
                self.linkQuence.addUnvisitedUrl(i)
        print "Add the seeds url \"%s\" to the unvisited url list"%str(self.linkQuence.unVisited)

    def crawling(self,seeds,crawl_count):

        while self.linkQuence.unVisitedUrlsEnmpy() is False and self.linkQuence.getVisitedUrlCount()<=crawl_count:
            visitUrl=self.linkQuence.unVisitedUrlDeQuence()
            print "Pop out one url \"%s\" from unvisited url list"%visitUrl
            if visitUrl is None or visitUrl=="":
                continue

            links=self.getHyperLinks(visitUrl)
            print "Get %d new links"%len(links)
            self.linkQuence.addVisitedUrl(visitUrl)
            print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())
            

    def getHyperLinks(self,url):
        links=[]
        data=self.getPageSource(url)
        if data[0]=="200":
            soup=BeautifulSoup(data[1])
            a=soup.findAll("a",{"href":re.compile(".*")})
            for i in a:
                if i["href"].find("http://")!=-1:
                    links.append(i["href"]) 
        return links
    
    def getPageSource(self,url,timeout=100,coding=None):
        try:
            socket.setdefaulttimeout(timeout)
            req = urllib2.Request(url)
            req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
            response = urllib2.urlopen(req)
            if coding is None:
                coding= response.headers.getparam("charset")
            if coding is None:
                page=response.read()
            else:
                page=response.read()
                page=page.decode(coding).encode('utf-8')
            return ["200",page]
        except Exception,e:
            print str(e)
            return [str(e),None]
        
class linkQuence:
    def __init__(self):
        self.visted=[]
        self.unVisited=[]

    def getVisitedUrl(self):
        return self.visted

    def getUnvisitedUrl(self):
        return self.unVisited

    def addVisitedUrl(self,url):
        self.visted.append(url)

    def removeVisitedUrl(self,url):
        self.visted.remove(url)

    def unVisitedUrlDeQuence(self):
        try:
            return self.unVisited.pop()
        except:
            return None

    def addUnvisitedUrl(self,url):
        if url!="" and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0,url)

    def getVisitedUrlCount(self):
        return len(self.visted)

    def getUnvistedUrlCount(self):
        return len(self.unVisited)

    def unVisitedUrlsEnmpy(self):
        return len(self.unVisited)==0
    
def main(seeds,crawl_count):
    craw=MyCrawler(seeds)
    craw.crawling(seeds,crawl_count)
if __name__=="__main__":
    main(["http://www.baidu.com","http://www.google.com.hk"],50)
