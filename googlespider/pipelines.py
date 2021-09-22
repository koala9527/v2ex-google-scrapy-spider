# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import codecs
import re,os

class GooglespiderPipeline(object):

    def process_item(self, item, spider):
        return item

class CsvspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('url.csv', 'w', encoding='utf_8_sig')

    def process_item(self, item, spider):
        fieldnames = ['url']
        w = csv.DictWriter(self.file, fieldnames=fieldnames)
        print(item)
        w.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()