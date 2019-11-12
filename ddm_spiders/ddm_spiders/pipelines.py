# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv, logging, time

class DdmSpidersPipeline(object):
    def process_item(self, item, spider):
        return item

class CsvWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('C:\\Test\\{}_{}.csv'.format(spider.name, time.strftime('%Y-%m-%d_T%H.%M')), 'w', newline='', encoding='utf8')
        self.items = []
        self.colnames = []

    def close_spider(self, spider):
        csvWriter = csv.DictWriter(self.file, fieldnames = self.colnames)
        logging.info("HEADER: " + str(self.colnames))
        csvWriter.writeheader()
        for item in self.items:
            csvWriter.writerow(item)
        self.file.close()

    def process_item(self, item, spider):
        for f in item.keys():
            if f not in self.colnames:
                self.colnames.append(f)
        self.items.append(item)
        return item