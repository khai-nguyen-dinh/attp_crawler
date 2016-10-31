# -*- coding: utf-8 -*-
import scrapy
import time

from vbpl.items import VbplItem


class Stackover(scrapy.Spider):
    name = 'vfa'
    allowed_domains = ['http://vfa.gov.vn','foodsafety.gov.vn']
    start_urls = [
        'http://vfa.gov.vn/doc/search?page=6'
    ]

    def parse(self, response):

        for url in response.xpath('//tr/td[3]/a/@href').extract():
            temp = VbplItem()
            slug = url.split('/')[-1]
            temp['slug'] = slug.split('.')[0]
            temp['url'] = url
            request = scrapy.Request(url, callback=self.parse_data, dont_filter=True)
            request.meta['item'] = temp
            yield request
        next_page = response.xpath('//a[@rel="prev"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_data(self, response):
        temp = response.meta['item'].copy()
        temp['title'] = response.xpath('//table[@class="table"]/tr[1]/td[2]/text()').extract_first()
        temp['code'] = response.xpath('//table[@class="table"]/tr[2]/td[2]/text()').extract_first()
        temp['date'] = response.xpath('//table[@class="table"]/tr[3]/td[2]/text()').extract_first()
        temp['date_active'] = response.xpath('//table[@class="table"]/tr[4]/td[2]/text()').extract_first()
        temp['company'] = response.xpath('//table[@class="table"]/tr[5]/td[2]/text()').extract_first()
        temp['category'] = response.xpath('//table[@class="table"]/tr[6]/td[2]/text()').extract_first()
        temp['file'] = response.xpath('//table[@class="table"]/tr[7]/td[2]/a/@href').extract_first()
        temp['lang'] = 'vn'
        url = 'http://foodsafety.gov.vn/crawl_document'
        request = scrapy.Request(url, callback=self.send_data, dont_filter=True)
        request.meta['item'] = temp
        yield request

    def send_data(self, response):
        temp = response.meta['item'].copy()
        token = response.xpath('//input[@name="_token"]/@value').extract_first()
        time.sleep(5)
        return scrapy.FormRequest.from_response(
            response, formdata={'_token': token, 'name': temp['title'], 'code': temp['code'],
                                'date_active': temp['date_active'], 'date': temp['date'], 'lang': temp['lang'], 'company': temp['company'],
                                'category_document': temp['category'],'file': temp['file'],'slug': temp['slug'],'link':temp['url']
                                }, callback=self.after_parse)

    def after_parse(self, response):
        print(response.body)