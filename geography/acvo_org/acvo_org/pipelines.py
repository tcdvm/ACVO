# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log


class AcvoOrgPipeline(object):
    def __init__(self):
        connection = pymongo.Connection(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            print data
            if not data:
                valid = False
                raise DropItem("Missing %s from %s" % (data, item['url']))
        if valid:
            print "Hi I'm in process_item!"
            self.collection.insert(dict(item))
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
            print "Item wrote to MongoDB database %s/%s" % (settings['MONGODB_DB'], settings['MONGODB_COLLECTION'])
            print item
        return item
