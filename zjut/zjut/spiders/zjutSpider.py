# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from zjut.items import ZjutItem
import re

class ZjutspiderSpider(scrapy.Spider):
    name = 'zjutSpider'
    allowed_domains = ['zjut.edu.cn']
    start_urls = ['http://www.zjut.edu.cn/BigClass.jsp?bigclassid=29']

    def parse_detail(self,response):
        items=ZjutItem()
        sel=Selector(response)
        items['url']=response.url
        items['title']=sel.xpath("//div[@class='newstitle'][@align='center']/text()").extract()[0]
        str1=u'来 源：'
        str2=u'日 期：'
        str3=u' 点击率：'
        inf=sel.xpath("//div[@align='center']/text()").extract()[0]
        inf=re.split(r'[str1|str2|str3]?',inf)
        items['author']=inf[0]
        items['date']=inf[1]
        yield items

    def parse(self, response):
        sel=Selector(response=response)#选择器的实例
        sites=sel.xpath("//div[@class='pictitle']")#选择器的实例组
        for site in sites:#遍历组中的每个选择器
            link=site.xpath("//a/@href").extract()[0]#extract返回list
            url_detail="http://www.zjut.edu.cn/%s"%(link)#生成新的url
            yield scrapy.Request(url_detail,callback=self.parse_detail)#二次爬取
        #sl=u'下一页'
        #url="http://www.zjut.edu.cn/"+sel.xpath("//a[text()='[%s]']/@href"%(sl)).extract()[0]
        #yield scrapy.Request(url,callback=self.parse)#爬取下一页
