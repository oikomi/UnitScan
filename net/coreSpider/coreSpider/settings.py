#!/usr/bin/python
#-*- coding: UTF-8 -*-
# Scrapy settings for coreSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'coreSpider'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['coreSpider.spiders']
NEWSPIDER_MODULE = 'coreSpider.spiders'
DEFAULT_ITEM_CLASS = 'coreSpider.items.CorespiderItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['coreSpider.pipelines.CorespiderPipeline']

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
DEPTH_LIMIT = 1


#for proxy
DOWNLOADER_MIDDLEWARES = {
'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
'coreSpider.middlewares.ProxyMiddleware': 100,
}


