# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class VbplPipeline(object):
    def process_item(self, item, spider):
        db = MySQLdb.connect(host="mysql",
                             user="ivtest_attp",
                             passwd="18101995",
                             db="ivtest_attp",
                             charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("""INSERT INTO tbl_document (c_name, c_date, c_date_active, c_company, c_category, c_file, c_lang, c_slug, c_code)
                            VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)""",
                           (item['title'].encode('utf-8'),
                            item['date'].encode('utf-8'),
                            item['date_active'].encode('utf-8'),
                            item['company'].encode('utf-8'),
                            item['category'].encode('utf-8'),
                            item['file'].encode('utf-8'),
                            item['lang'].encode('utf-8'),
                            item['slug'],
                            item['code'].encode('utf-8')))

            db.commit()
            return item
        except MySQLdb.Error:
            print
            "Error import database"
            return item