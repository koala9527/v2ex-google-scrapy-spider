# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from googlespider.items import GooglespiderItem


class V2exSpider(scrapy.Spider):
    name = 'v2ex' #爬虫名字。启动时候会用到它
    allowed_domains = ['google.com'] #限制这个爬虫程序爬取内容的域名，在复杂的爬虫中有很多情况会爬到其他站点去
    start_urls = ['http://google.com/'] #自动生成的爬虫程序开始爬取的域名，一般不用它。
    page_data = 10  #google 的翻页页数。相当于全局变量，后面的程序改变它使用它

    #这里设置公用的headers是因为v2ex这个网站使用默认的headers请求状态直接403了，不让你访问，后面会补充这个header是如何生成的
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
        # 这个函数是自己的写的，也是scrapy认可的，一开始会执行这个函数
        #这个url是google的搜索页，site和inititle是google的高级搜索方法关键字，site指搜索结果只包含某个站点，intitle只搜索关键字之存在搜索结果网页的标题中
        url = "https://www.google.com/search?q=site:v2ex.com/t+intitle:%E4%B8%AD%E7%A7%8B"
        # yield这是Python的高级用法，迭代器，这里就是实现异步爬虫的关键要点，把这个url的请求解析工作交给了parse这个方法，当前函数可以继续向下执行，但是这里是没有下面的方法了，然后迭代器又有很多迭代器。就会出现很对的异步请求。
        yield Request(url,  callback=self.parse)

    def parse(self, response):
        # response对象是scrapy封装的对象，这里面有好多对象方法，例如下面的.selector.re就是使用正则提取网页关键内容的方法，我们提取google第一页的文章链接
        url_list = response.selector.re("https://www.v2ex.com/t/[0-9]*")
        print(url_list)
        # 如果有文章链接就解析链接，把请求文章详情的任务用异步任务交给下一个方法去完成，然后翻页，直到google的结果页再也没有文章链接了
        if(len(url_list) > 0):
            for i in url_list:
                yield Request(url=i, callback=self.parse_detail, dont_filter=True,headers=self.headers)
            yield Request(url="https://www.google.com/search?q=site:v2ex.com/t+intitle:%E4%B8%AD%E7%A7%8B&start="+str(self.page_data), callback=self.parse)
            self.page_data += 10

    def parse_detail(self, response):
        # 这里使用xpath来解析v2ex文章内容。下面截图会补充
        xpath_str = '//*[@class="reply_content"]/text()'
        # 这里是收集爬去数据的管道，这个item管道会把数据交给下载器，下载器的后面编写下面接着说
        item = GooglespiderItem()
        word_list = response.xpath(xpath_str).getall()
        if(len(word_list)>0):
            for i in word_list:
                
                item['word'] = i
                #把爬取的内容交给管道，管道会把数据自动调度给下载器使用
                yield item
