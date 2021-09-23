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
        # 构造方法打开一个csv文件，不存在就创建
        self.file = codecs.open('word.csv', 'w', encoding='utf_8_sig')

    def process_item(self, item, spider):
        fieldnames = ['word']
        w = csv.DictWriter(self.file, fieldnames=fieldnames)
        print(item) #这里是一个字典
        #写入文件
        w.writerow(item)
        return item

    def close_spider(self, spider):
        # 关闭文件
        self.file.close()