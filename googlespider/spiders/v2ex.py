# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from googlespider.items import GooglespiderItem


class V2exSpider(scrapy.Spider):
    name = 'v2ex'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/', 'https://www.v2ex.com/']
    page_data = 10
    headers = {
        'authority': 'www.v2ex.com',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'image',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'PB3_SESSION="2|1:0|10:1632320639|11:PB3_SESSION|36:djJleDo0Ny4yNTQuODQuMjA2Ojk5NTgyNDE3|af262dbef778709e4964d0dec124e60e267c03ac8e01bf98e702cb85b7fd0698"; V2EX_LANG=zhcn; _ga=GA1.2.2017158286.1632320642; _gid=GA1.2.1291035321.1632320642; A2="2|1:0|10:1632321211|2:A2|48:M2RjYzkzMWQtOTAwZi00YTA4LWEyNTctZmQ2NTdiMmY4YmMy|b75429367c29090d8e1b29d8f3c84a7c5e723005928c6d5267e4137e6bc02e91"; V2EX_REFERRER="2|1:0|10:1632321220|13:V2EX_REFERRER|8:VG9ieTIz|fbb0b7efd4f44fcd4298c61978cf3a395fd7111e54d8185344e5e8d286dff7f4"; V2EX_TAB="2|1:0|10:1632327619|8:V2EX_TAB|8:dGVjaA==|90bd1f7b91355e424c24b6192cbef107cde9747006042d46320b41b0b991173d"; _gat=1',
        'Referer': 'https://www.v2ex.com/t/710481',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'referer': 'https://www.v2ex.com/t/710481',
        'Origin': 'https://www.v2ex.com',
        'if-modified-since': 'Wed, 11 Aug 2021 00:32:57 GMT',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'content-length': '0',
        'content-type': 'text/plain',
        'origin': 'https://www.v2ex.com',
        'if-none-match': 'W/"55467a007c0429c0b04e98443edd5063d10f0b22"',
        'pragma': 'no-cache',
        'Content-Type': 'text/plain',
    }

    def start_requests(self):
        url = "https://www.google.com/search?q=site:v2ex.com/t+intitle:%E4%B8%AD%E7%A7%8B"
        yield Request(url,  callback=self.parse)

    def parse(self, response):
        # print(response.text)
        url_list = response.selector.re("https://www.v2ex.com/t/[0-9]*")
        print(url_list)

        if(len(url_list) > 0):
            for i in url_list:

                yield Request(url=i, callback=self.parse_detail, dont_filter=True,headers=self.headers)
            yield Request(url="https://www.google.com/search?q=site:v2ex.com/t+intitle:%E4%B8%AD%E7%A7%8B&start="+str(self.page_data), callback=self.parse)
            self.page_data += 10

    def parse_detail(self, response):
        print("jinlaile!!!!!!!111")
        xpath_str = '//*[@class="reply_content"]'
        item = GooglespiderItem()
        word_list = response.xpath(xpath_str)
        if(len(word_list)>0):
            for i in word_list:
                
                item['word'] = i
                yield item
