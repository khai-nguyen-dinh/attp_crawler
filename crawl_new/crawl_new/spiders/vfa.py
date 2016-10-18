# -*- coding: utf-8 -*-
import scrapy
import time

from crawl_new.items import CrawlNewItem


class Stackover(scrapy.Spider):
    name = 'vfa'
    allowed_domains = ['http://vfa.gov.vn','foodsafety.gov.vn']
    start_urls = [
        'http://vfa.gov.vn/tin-tuc.html'
    ]

    def parse(self, response):

        for rel in response.xpath('//div[@class="categorylist"]/div/div'):
            temp = CrawlNewItem()
            url = rel.xpath('div[1]/a/@href').extract_first().strip()
            temp['image'] = rel.xpath('div[1]/a/img/@src').extract_first().strip()
            temp['date'] = rel.xpath('div[2]/div[@class="timer hidden-xs"]/text()').extract_first('').strip()
            temp['description'] = rel.xpath('div[2]/p/text()').extract_first('').strip()
            temp['title'] = rel.xpath('div[2]/h2/a/text()').extract_first('').strip()
            slug = url.split('/')[-1]
            temp['slug'] = slug.split('.')[0]
            request = scrapy.Request(url, callback=self.parse_data, dont_filter=True)
            request.meta['item'] = temp
            yield request

        # next_page = response.xpath('//a[@rel="next"]/@href')
        # if next_page:
        #     url = response.urljoin(next_page.extract_first())
        #     yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_data(self, response):
        temp = response.meta['item'].copy()
        temp['lang'] = 'vn'
        temp['content'] = response.xpath('//div[@class="fulltext"]').extract()
        temp['content'] = ''.join(response.xpath('//h2[@class="introtext"]').extract() + temp['content'])
        url = 'http://foodsafety.gov.vn/crawl_news'
        request = scrapy.Request(url, callback=self.send_data,dont_filter=True)
        request.meta['item'] = temp
        yield request

    def send_data(self, response):
        temp = response.meta['item'].copy()
        token = response.xpath('//input[@name="_token"]/@value').extract_first()
        time.sleep(5)
        return scrapy.FormRequest.from_response(
            response, formdata={'_token': token, 'name': temp['title'], 'description': temp['description'],
                                'lang': 'vn', 'slug': temp['slug'], 'date': temp['date'], 'img': temp['image'],'content':temp['content']
                                }, callback=self.after_parse)

    def after_parse(self, response):
        print(response.body)
