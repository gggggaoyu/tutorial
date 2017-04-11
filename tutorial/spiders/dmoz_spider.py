# coding:utf-8
import scrapy
from scrapy.http import FormRequest
from faker import Factory
from tutorial.items import DmozItem
import urlparse
import re
import urllib2
import urllib
import requests

f = Factory.create()

# from scrapy import log
# scrapy.log.start(logstdout=True)
# scrapy.log.msg("This is a warning", level=log.DEGUG)

class DmozSpider(scrapy.Spider):
    name = "cisco1"
    allowed_domains = ["cisco.com"]


    start_urls = [
       'https://sso.cisco.com/autho/login/loginaction.html',
    ]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'sso.cisco.com',
        'User-Agent': f.user_agent(),
    }

    formdata = {
        'userid': 'wangyang',
        'password': 'p@ssW0RD88',
        # 'target':'',
        # 'smauthreason':'',
        # 'smquerydata':'',
        # 'smagentname':'',
        # 'postpreservationdata':'',
        # 'SMENC':'',
        # 'SMLOCALE':'',
        #'source': 'index_nav',
        #'Referer': 'https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
    }

    def start_requests(self):
        return [scrapy.FormRequest(url='https://sso.cisco.com/autho/login/loginaction.html',
                                #url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                               formdata = self.formdata,
                               headers = self.headers,
                               meta={'cookiejar': 1},
                               callback=self.after_login)]

    def after_login(self, response):
        # title = response.xpath('//*[@id="cmDataDiv"]/table/tbody/tr[1]/td[2]/a/@href').extract()[0][1:]
        # print title
        # print "after_login"
        return [scrapy.FormRequest(url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                                   meta={'cookiejar': response.meta['cookiejar']},
                                   callback=self.contract_manager_login)]

    def contract_manager_login(self, response):
        pass
        info = DmozItem()
        #info['title'] = response.xpath('//*[@id="cmDataDiv"]/table/tbody/tr[1]/td[2]/a').extract()[0]
        info['title'] = response.xpath('//*[@id="cmDataDiv"]/table/tbody/tr[1]/td[2]/a/@href').extract()[0][1:]
        # info['link'] = response.xpath('#cmDataDiv > table > tbody > tr:nth-child(3) > td:nth-child(2) > a').extract()[0]
        # info['desc'] = response.xpath('//title[1]//text()').extract()[0]
        url2  = 'https://apps.cisco.com/CustAdv/ServiceSales/contract'+ info['title']
        print info['title']
        return [scrapy.FormRequest(url2,
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.manager_login)]

    def manager_login(self, response):
        list = []
        title_href = response.xpath('//title[1]').extract()[0]
        #ContractNumber = response.xpath('//*[@id="ContractNumber"]').extract()[0]
        # //*[@id="ServiceLineId"]

        self.ContractNumber = response.xpath('//*[@id="ContractNumber"]/@value').extract()
        self.seqId = response.xpath('//*[ @ id = "seqId"]/@value').extract()
        self.ServiceLineId = response.xpath('//*[@id="ServiceLineId"]/@value').extract()
        script_text = response.xpath('//*[@id="mod_1"]/script/text()').extract()[0]
        # print script_text
        url_half = re.compile('case\s\'Download Contract or Selected Data\':[\s|\S]*?url = checkBrowser\(\'(.*?)\'\);').findall(script_text)[0]
        print url_half
        print type(url_half)
        url3 = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/' + url_half
        print url3
        return [scrapy.FormRequest(url3,
                                   meta={'cookiejar': response.meta['cookiejar']},
                                   callback=self.download_page
                                   )]

    def download_page(self, response):
        self.formdata_b = {
            'seqId': self.seqId,
            'PageId': '2',
            'page': 'CS',
            'ContractNumber': self.ContractNumber,
            'ServiceLineId': self.ServiceLineId,
            'ContractType': 'HW',
            'selProdType': 'MAJOR',
            'EQT': '',
            'userType': '',
            'downloadMethod': 'SAVE',
            'Config': 'MINOR',
            'emailTo': 'service @ nantian.com.cn',
            'emailCC': '',
        }
        print "已经进入下载页面"
        title_href = response.xpath('//title[1]').extract()[0]
        title = response.xpath('//title[1]/text()').extract()[0]
        print title
        # return [scrapy.FormRequest.from_response(response,
        #                                          formdata=self.formdata,
        #                                          #headers=self.headers,
        #                                          meta={'cookiejar': response.meta['cookiejar']},
        #                                          callback=self.download_result
        #                                          )]
        return [scrapy.FormRequest(url='https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm',
                                   # url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                                   formdata=self.formdata_b,
                                   meta={'cookiejar': response.meta['cookiejar']},
                                   callback=self.download_result
                                   )]
        # url_load = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm'
        # pppp = requests.post(url_load, headers = resopnse.request.,data = self.formdata_b)
        # print pppp


    def download_result(self, response):
        list = []
        # title_href = response.xpath('//title[1]').extract()[0]
        # title = response.xpath('//title[1]/text()').extract()[0]
        print (response.url)
        print dir(response.request)
        print response.headers
        print "这个是返回了什么呢？"
        #requests.get('response.url')  # GET请求
        #r = requests.get(response.url, headers = response.request.headers)
        #print dir(r)
        #print r.text
        # return [scrapy.FormRequest(response.url,
        #                                          #formdata=self.formdata_b,
        #                                          #headers=self.headers,
        #                                          meta={'cookiejar': response.meta['cookiejar']},
        #                                          callback=self.after_login
        #                                          )]
        return [scrapy.FormRequest(
            url='https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm',
            # url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
            formdata=self.formdata_b,
            meta={'cookiejar': response.meta['cookiejar']},
            dont_filter=True,
            callback=self.after_download
            )]

    def after_download(self, response):
        #list = []
        # title_href = response.xpath('//title[1]').extract()[0]
        # title = response.xpath('//title[1]/text()').extract()[0]
        print (response.url)
        print dir(response.request)
        #print "这个是返回了什么呢？"
        r = requests.get(response.url, headers = response.request.headers)
        print dir(r)
        print type(r.content)
        r.encoding = 'utf-8'
        print r.content
        print "it's over!"
        print r.text
        # return [scrapy.FormRequest.from_response(response,
        #                                          formdata=self.formdata,
        #                                          headers=self.headers,
        #                                          meta={'cookiejar': response.meta['cookiejar']},
        #                                          callback=self.after_login
        #                                          )]
        # print response.body.decode(response.encoding)
        # title_href = response.xpath('//title[1]').extract()[0]
        # title = response.xpath('//title[1]/text()').extract()[0]
        # print title
        # print title_href
        # 这个是真正提交的网址，方法是POST
        # https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm

