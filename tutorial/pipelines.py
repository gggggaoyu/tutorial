# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import
# 可以定义多个Item,使用的时候可以这样来判断
# if isinstance(item, Aitem):
#     pass
# elif isinstance(item, Bitem):
#     pass
# else:
#     pass
from tutorial.items import StreamItem
import requests


class TutorialPipeline(object):
    pass
    # def open_spider(spider):
    #     pass
    #
    # def close_spider(spider):
    #     pass
    #
    # def process_item(self, item, spider):
    #     if isinstance(item, StreamItem):
    #         item['name'] = item['name']
    #         r = requests.get(item[''], headers = response.request.headers)
    #
    #         print dir(r)
    #         with open(r'e:' + self.ContractNumber + '.zip', 'wb') as code:
    #             code.write(r.content)
    #         item
        # elif isinstance(item, Bitem):
        #     pass
        # else:
        # return item


#from scrapy.exceptions import DropItem

# class DuplicatesPipeline(object):
#
#     def __init__(self):
#         self.ids_seen = set()
#
#     def process_item(self, item, spider):
#         if item['id'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             return item
#
# import json
#
# class JsonWriterPipeline(object):
#     def __init__(self):
#         self.file = open('items.jl', 'wb')
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item


# class ContractWriterPipeline(object):
#     # def __init__(self):
#     #     self.file = open('items.jl', 'wb')
#
#     def process_item(self, item, spider):
#         # line = json.dumps(dict(item)) + "\n"
#         # self.file.write(line)
#         return item

# class PricePipeline(object):
#     vat_factor = 1.15
#
#     def process_item(self, item, spider):
#         if item['price']:
#             if item['price_excludes_vat']:
#                 item['price'] = item['price'] * self.vat_factor
#             return item
#         else:
#             raise DropItem("Missing price in %s" % item)
