# Scrapy settings for acvo_org project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'acvo_org'

SPIDER_MODULES = ['acvo_org.spiders']
NEWSPIDER_MODULE = 'acvo_org.spiders'

ITEM_PIPELINES = {
    'acvo_org.pipelines.AcvoOrgPipeline': 300,
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "acvo_14"
MONGODB_COLLECTION = "diplomates"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'acvo_org (+http://www.yourdomain.com)'
