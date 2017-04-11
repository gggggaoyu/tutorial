# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 可以定义多个Item,使用的时候可以这样来判断
# if isinstance(item, Aitem):
#     pass
# elif isinstance(item, Bitem):
#     pass
# else:
#     pass
class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    tableID = scrapy.Field()
    contextID = scrapy.Field()
    pages = scrapy.Field()

# 进入合同管理页面
class DmozItem2(scrapy.Item):
    title2 = scrapy.Field()
    url_manager = scrapy.Field()

# 获取管理合同的每一页地址
class PageItem(scrapy.Item):
    title = scrapy.Field()
    url_page = scrapy.Field()

# 获取每一页里面所有合同的管理地址
class DmozItem4(scrapy.Item):
    title2 = scrapy.Field()
    url_contract = scrapy.Field()


# 获取每一个合同下载的地址的需要提交的信息和提交的真正地址,即Go
class DmozItem5(scrapy.Item):
    title = scrapy.Field()
    url_really = scrapy.Field()


# 点击product+con 点击save now 点击sumbit 提交一次后获得了提交参数和submit的地址
class SumbitItem(scrapy.Item):
    seqId = scrapy.Field()
    ServiceLineId = scrapy.Field()
    ContractNumber = scrapy.Field()
    url_sumbit = scrapy.Field()

# 提交二次后获得了一个新的地址，再对这个地址访问后就生成了一个流，需要保存一下
class StreamItem(scrapy.Item):
    title = scrapy.Field()
    stream = scrapy.Field()