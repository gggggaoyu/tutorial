# coding:utf-8
import re
import requests
import scrapy
#from tutorial import DmozItem
from faker import Factory
from tutorial.items import DmozItem
#PageItem,SumbitItem

f = Factory.create()


class DmozSpider(scrapy.Spider):
    name = "cisco"
    allowed_domains = ["cisco.com"]

    start_urls = [
       #'https://sso.cisco.com/autho/login/loginaction.html',
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
    contract_urls = []
    contract_go_urls = []
    contract_pages_url = []

    def start_requests(self):
        return [scrapy.FormRequest(url='https://sso.cisco.com/autho/login/loginaction.html',
                                #url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                               formdata=self.formdata,
                               headers=self.headers,
                               meta={'cookiejar': 1},
                               callback=self.after_login)]

    def after_login(self, response):
        print "after_login"

        return [scrapy.FormRequest(url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                                   meta={'cookiejar': response.meta['cookiejar']},
                                   callback=self.parse_contract_manager)]

    # 进入合同管理页面
    count = 0
    def parse_contract_manager(self, response):
        if self.count == 0:
            self.tableID = response.xpath('//*[@id = "tableIdForActions"]/@value').extract()[0]
            self.contextID = response.xpath('//*[@id = "cmContextForActions"]/@value').extract()[0]
            self.pages = response.xpath('//*[@id = "mod_2"]/table/tbody/tr/td[2]/text').extract()
            self.count = self.count +1
        # info['href'] = response.xpath('//*[@id="cmDataDiv"]/table/tbody/tr[1]/td[2]/a/@href').extract()[0][1:]
        # info['link'] = response.xpath('#cmDataDiv > table > tbody > tr:nth-child(3) > td:nth-child(2) > a').extract()[0]
        # info['ContractNumber'] = response.xpath('//*[@id="cmDataDiv"]/table/tbody/tr[1]/td[2]/a/text').extract()[0]
        print self.tableID
        print self.contextID
        for page in range(1):
            page_url = r'https://apps.cisco.com/CustAdv/ServiceSales/contract/performTableActions.do?sortID=contractNumber&pageID=' + str(
                page + 1) + '&tableID=' + self.tableID + '&contextID=' + self.contextID + '&method=paginateContracts&cmToLine=undefined&selectedProductsCHR=&currentPageId=1'
            self.contract_pages_url.append(page_url)

        list1 = self.collect_urls(self)
        for res in list1:
            response = res.response
            items = response.xpath('//*[@id="cmDataDiv"]/table/tbody/tr')
            print items
            print len(items)
            for item in items:
                if item.xpath('td[2]/a/@href').extract():
                    value_test = item.xpath('td[2]/a/@href').extract()[0]
                    print value_test
                    value = item.xpath('td[2]/a/@href').extract()[0][1:]
                    # print "是什么"
                    url = 'https://apps.cisco.com/CustAdv/ServiceSales/contract' + value
                    print url
                    self.contract_urls.append(url)

        # 这里怎么能用上生成器，那就暂时先用scrapy保存一下cookies。
        list2 = self.enter_contract(self,response)
        for co_url in list2:
            response = list2.co_url
            # 选取合同后，进入合同内容中心
            title_href = response.xpath('//title[1]').extract()[0]
            print "返回了什么"
            script_text = response.xpath('//*[@id="mod_1"]/script/text()').extract()[0]
            # print script_text
            url_half = re.compile(
                'case\s\'Download Contract or Selected Data\':[\s|\S]*?url = checkBrowser\(\'(.*?)\'\);').findall(
                script_text)[0]
            print url_half
            print type(url_half)
            url3 = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/' + url_half
            print url3
            # 进入待下载页面
            self.contract_go_urls.append(url3)

        list3 = self.contract_go(self,response)
        for con_url in self.contract_go_urls:
            response = list2.co_url
            # sumbititem = SumbitItem()
            # sumbititem['seqId'] = response.xpath('//*[ @ id = "seqId"]/@value').extract()[0]
            self.seqId = response.xpath('//*[ @ id = "seqId"]/@value').extract()[0]
            # sumbititem['ServiceLineId'] = response.xpath('//*[@id="ServiceLineId"]/@value').extract()[0]
            self.ServiceLineId = response.xpath('//*[@id="ServiceLineId"]/@value').extract()[0]
            # sumbititem['ContractNumber'] = response.xpath('//*[@id="ContractNumber"]/@value').extract()[0]
            self.ContractNumber = response.xpath('//*[@id="ContractNumber"]/@value').extract()[0]
            print self.ContractNumber
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
            # SumbitItem['formdata'] = self.formdata
            print "设置完参数等待下载"
            title_href = response.xpath('//title[1]').extract()[0]
            title = response.xpath('//title[1]/text()').extract()[0]
            print title
            # return SumbitItem
            # 提交新的formdata,请求真正的URL，action是下载
            url_submmit ='https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm'
            r = requests.post(url_submmit, headers=response.request.headers,data=self.formdata_b)
            print dir(r)
            # r = requests.get(response.url, headers=response.request.headers)
            # print dir(r)
            # with open(r'e:' + self.ContractNumber + '.zip', 'wb') as code:
            #     code.write(r.content)

    def collect_urls(self,response):
        for x in self.contract_pages_url:
            yield scrapy.FormRequest(url=x,meta={'cookiejar': response.meta['cookiejar']},
            callback=self.collect_urls)

    def enter_contract(self,response):
        for x in self.contract_urls:
            yield scrapy.FormRequest(url=x, meta={'cookiejar': response.meta['cookiejar']},
                                     callback=self.enter_contract)

    def contract_go(self,response):
        for x in self.contract_urls:
            yield scrapy.FormRequest(url=x,
                                     meta={'cookiejar': response.meta['cookiejar']},
                                     callback=self.contract_go)


    # 选取下载合同的选项，点击GO
    # 点击product+con 点击save now 点击sumbit
    # 返回了一个地址，测试请求这个地址
    # print r.raw
    # r.encoding = 'utf-8'
    # print r.content
    # print "it's over!"
    # #print r.text
    # print type(StringIO.StringIO(r.context))

    # print response.body.decode(response.encoding)
    # 这个是最后提交的网址，方法是POST
    # https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm

