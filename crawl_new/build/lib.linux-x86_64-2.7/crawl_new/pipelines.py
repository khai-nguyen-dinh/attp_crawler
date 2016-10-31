# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class CrawlNewPipeline(object):
    def process_item(self, item, spider):
        db = MySQLdb.connect(host="mysql",
                        user="ivtest_attp",
                        passwd="18101995",
                        db="ivtest_attp",
                        charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("""INSERT INTO tbl_news (c_name, c_description, c_content, c_img, c_date, c_view, c_lang, c_category_news, c_slug)
                            VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)""",
                                (item['title'].encode('utf-8'),
                                 item['description'].encode('utf-8'),
                                 item['content'].encode('utf-8'),
                                 item['image'].encode('utf-8'),
                                 item['date'].encode('utf-8'),
                                 item['view'],
                                 item['lang'].encode('utf-8'),
                                 item['category'],
                                 item['slug'].encode('utf-8')))

            db.commit()
            return item
        except MySQLdb.Error:
            print
            "Error import database"
            return item
