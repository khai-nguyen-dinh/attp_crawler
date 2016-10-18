# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VbplItem(scrapy.Item):
   title = scrapy.Field()
   date = scrapy.Field()
   date_active = scrapy.Field()
   company = scrapy.Field()
   category = scrapy.Field()
   file = scrapy.Field()
   lang = scrapy.Field()
   slug = scrapy.Field()
   code = scrapy.Field()