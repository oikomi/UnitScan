#!/usr/bin/env python
# -*- coding: utf-8 -*-


import threading
import GetUrl
import urllib

g_mutex = threading.Lock()
g_pages = []      
g_dledUrl = []    
g_toDlUrl = []    
g_failedUrl = [] 
g_totalcount = 0  

#miaohong add
def getUrl():
    return g_dledUrl

class WebCrawler:
    def __init__(self,threadNumber,Maxdepth):
        self.threadNumber = threadNumber
        self.threadPool = []
        self.Maxdepth = Maxdepth
        self.logfile = file('#log.txt','w')                                  

    def download(self, url, fileName):
        Cth = CrawlerThread(url, fileName)
        self.threadPool.append(Cth)
        Cth.start()

    def downloadAll(self):
        global g_toDlUrl
        global g_totalcount
        i = 0
        while i < len(g_toDlUrl):
            j = 0
            while j < self.threadNumber and i + j < len(g_toDlUrl):
                g_totalcount += 1   
                self.download(g_toDlUrl[i+j],str(g_totalcount)+'.htm')
                print 'Thread started:',i+j,'--File number = ',g_totalcount
                j += 1
            i += j
            for th in self.threadPool:
                th.join(30)    
            self.threadPool = []   
        g_toDlUrl = []   

    def updateToDl(self):
        global g_toDlUrl
        global g_dledUrl
        newUrlList = []
        for s in g_pages:
            newUrlList += GetUrl.GetUrl(s)  
        g_toDlUrl = list(set(newUrlList) - set(g_dledUrl))    
                
    def Craw(self,entryUrl):   
        g_toDlUrl.append(entryUrl)
        self.logfile.write('>>>Entry:\n')                                      
        self.logfile.write(entryUrl)                                           
        depth = 0
        while len(g_toDlUrl) != 0 and depth <= self.Maxdepth:
            depth += 1
            print 'Searching depth ',depth,'...\n\n'
            self.downloadAll()
            self.updateToDl()
            content = '\n>>>Depth ' + str(depth)+':\n'                         
            self.logfile.write(content)                                        
            i = 0                                                              
            while i < len(g_toDlUrl):                                          
                content = str(g_totalcount + i + 1) + '->' + g_toDlUrl[i] + '\n'
                self.logfile.write(content)                                    
                i += 1                                                        
         
class CrawlerThread(threading.Thread):
    def __init__(self, url, fileName):
        threading.Thread.__init__(self)
        self.url = url    
        self.fileName = fileName

    def run(self):    
        global g_mutex
        global g_failedUrl
        global g_dledUrl
        try:
            f = urllib.urlopen(self.url)
            s = f.read()
            fout = file(self.fileName, 'w')
            fout.write(s)
            fout.close()
        except:
            g_mutex.acquire()    
            g_dledUrl.append(self.url)
            g_failedUrl.append(self.url)
            g_mutex.release()   
            print 'Failed downloading and saving',self.url
            return None  
        
        g_mutex.acquire()   
        g_pages.append(s)
        g_dledUrl.append(self.url)
        g_mutex.release()   
