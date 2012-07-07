#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from net.coreSpider.coreSpider.spiders.coreSpider import main_cmd
import os
import sys

def main():

    cmd = "scrapy crawl coreSpider"
    #os.chdir("../.")
    oDir = os.getcwd()
    os.chdir(os.getcwd()+"/net/coreSpider/")
    print os.getcwd()
    os.system(cmd)
    os.chdir(oDir)


if __name__ == '__main__':
    main()