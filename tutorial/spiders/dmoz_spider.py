# coding:utf-8
import scrapy
from scrapy.http import FormRequest
from faker import Factory
from tutorial.items import DmozItem
import urlparse

import log
log.set_logger(level = 'DEBUG')
f = Factory.create()


class DmozSpider(scrapy.Spider):
    name = "cisco"
    allowed_domains = ["cisco.com"]

    start_urls = [
       # "https://www.douban.com/",
    ]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'sso.cisco.com',
        'User-Agent': f.user_agent(),
    }

    formdata = {
        # 'form_email': 'wangyang',
        # 'form_password': 'p@ssW0RD88',
        'userid': 'wangyang',
        'password': 'p@ssW0RD88',
        # 'target':'',
        # 'smauthreason':'',
        # 'smquerydata':'',
        # 'smagentname':'',
        # 'postpreservationdata':'',
        # 'SMENC':'',
        # 'SMLOCALE':'',
        # 'source': 'index_nav',
    }

    def start_requests(self):
        log.debug("start")
        return [scrapy.FormRequest(url='https://sso.cisco.com/autho/login/loginaction.html',
                                formdata = self.formdata,
                               headers = self.headers,
                               meta={'cookiejar': 1},
                               callback=self.parse_login)]

    def parse_login(self, response):
        log.debug(response)

        return [scrapy.FormRequest.from_response(response,
                                   meta = {'cookiejar' : response.meta['cookiejar']},
                                   formdata=self.formdata,
                                   callback=self.after_login)]

    def after_login(self, response):

        url = "https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr"
        log.debug(url)

        return [scrapy.FormRequest(url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                                   meta={'cookiejar': response.meta['cookiejar']},
                                   callback=self.last_login)]

    def last_login(self, response):
        
        log.debug(response.xpath('//title').extract()[0])
