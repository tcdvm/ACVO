# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AcvoDipItem(Item):
    username       = Field()
    url            = Field()
    firstname      = Field()
    lastname       = Field()
    worktype       = Field()
    addresses      = Field()
    dateupdated    = Field()
    # horses         = Field()
    # birds          = Field()
    # exotics        = Field()
    # other          = Field()
    # speaker        = Field()
    # speaker_topics = Field()
    # eyeregistry    = Field()
