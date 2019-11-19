# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv, logging, time, shutil

class DdmSpidersPipeline(object):
    def process_item(self, item, spider):
        return item

class CsvWriterPipeline(object):

    def open_spider(self, spider):
        self.file_path = 'C:\\Test\\{}_{}.csv'.format(spider.name, time.strftime('%Y-%m-%d_T%H.%M'))
        self.file = open(self.file_path, 'w', newline='', encoding='utf8')
        self.items = []
        self.colnames = []

    def close_spider(self, spider):
        csvWriter = csv.DictWriter(self.file, fieldnames = self.colnames)
        logging.info("HEADER: " + str(self.colnames))
        csvWriter.writeheader()
        for item in self.items:
            csvWriter.writerow(item)
        self.file.close()
        if spider.name == 'sitescraper':
            self.dest_path = r'C:\Users\Distristo\Documents\Repos\Distrito Dataminer\Scripts'
            shutil.copy(self.file_path, self.dest_path+'\\ss_results.csv')
        elif spider.name == 'lkdscraper':
            self.dest_path = r'C:\Users\Distristo\Documents\Repos\Distrito Dataminer\Scripts'
            shutil.copy(self.file_path, self.dest_path+'\\lkd_results.csv')

    def process_item(self, item, spider):
        for f in item.keys():
            if f not in self.colnames:
                self.colnames.append(f)
        self.items.append(item)
        return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        
        self.file = open('C:\\Test\\all_jsons.txt', 'w', encoding='utf8')

        for item in self.items:
            self.file.write(item.get('content'))
            self.file.write('\n---SEPARATOR---\n')
        
        for item in self.items:
            with open('C:\\Test\\SB\\{}.json'.format(item.get('name')), 'w', encoding='utf8') as f:
                f.write(item.get('content'))
                f.close()

    def process_item(self, item, spider):
        self.items.append(item)
        return item