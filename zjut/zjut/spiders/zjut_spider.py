# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from zjut.items import zjutItem

class ZjutSpiderSpider(scrapy.Spider):
    name = 'zjut_spider'
    allowed_domains = ['zjut.edu.cn']
    start_urls = ['http://www.zjut.edu.cn/BigClass.jsp?bigclassid=10']

    def parse_detail(self,response):
        sel=Selector(response)
        item=zjutItem()
        item['url']=response.url
        item['title']=sel.xpath("//div[@align='center'][@class='newstitle']/text()").extract()[0]
        yield item

    def parse(self, response):
        sel=Selector(response)
        sites=sel.xpath("//span[@class='news']")
        for site in sites:
            link =site.xpath("a/@href").extract()[0]
            url_detail = "http://www.zjut.edu.cn/%s" % (link)
            yield scrapy.Request(url_detail)
        sl=u'下一页'
        url="http://www.zjut.edu.cn/"+sel.xpath("//a[text()='[%s]']/@href" % (sl)).extract()[0]
        yield scrapy.Request(url,callback=self.parse)
