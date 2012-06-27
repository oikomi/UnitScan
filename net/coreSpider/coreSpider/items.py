# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CorespiderItem(Item):
    # define the fields for your item here like:
    url = Field()
    header = Field()
    form = Field()
    
