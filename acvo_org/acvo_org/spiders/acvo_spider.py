from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
# from scrapy.item import Item
# import lxml.html as lxml
from acvo_org.items import AcvoDipItem
# from numpy import loadtxt


class AcvoSpider(CrawlSpider):
    name = 'acvo'
    allowed_domains = ['acvo.org', 'member.acvo.org', ]
    start_urls = [
        ("http://member.acvo.org/search_results?country=usa&state=&city=&map=1&list=1"),
        ("http://member.acvo.org/search_results?page=1&country=usa&region=&state=&city=&map=1&list=1"),
        ("http://member.acvo.org/search_results?page=2&country=usa&region=&state=&city=&map=1&list=1"),
        ("http://member.acvo.org/search_results?page=3&country=usa&region=&state=&city=&map=1&list=1"),
        ("http://member.acvo.org/search_results?page=4&country=usa&region=&state=&city=&map=1&list=1")
        # ("http://member.acvo.org/search_results?country=USA&region=&state=CO&city=&map=1&list=1")
        # ("http://member.acvo.org/search_results?country=USA&region=&state=AK&city=&map=1&list=1")
    ]

    rules = [
        # Rule(SgmlLinkExtractor(allow=[r'search_results']), follow=True),
        Rule(
            SgmlLinkExtractor(allow=(r'users'),
                              canonicalize=True,
                              unique=True,
                              attrs=["href"]),
            callback='parse_dip',
            # follow=True
        ),
    ]

    def parse_dip(self, response):
        acvodip = AcvoDipItem()
        print "\nhi! ## %s ##\n" % response.url
        sel = Selector(response)
        fieldsets = sel.xpath('//fieldset')

        try:
            date = sel.xpath('//div[@class="meta"]/p/text()').re(
                "on (\w\w\w, \d\d\d\d-\d\d-\d\d)"
            )
            acvodip['dateupdated'] = date[0].strip() if len(date) > 0 else None

            dip_username = sel.xpath(
                '//h1[contains(@class, "title")]/text()'
            ).extract()
            print "=============\n" + dip_username[0] + "\n-------------"
            acvodip['username'] = dip_username[0].strip()

            acvodip['firstname'] = fieldsets[0].re("Dr. (\w+[\s*\w*]*\.?)")[0].strip()
            print "First name:\t" + "\'" + acvodip['firstname'] + "\'"

            acvodip['lastname'] = fieldsets[0].re("Last name:.*\s*(\w+)")[0].strip()
            print "Last name:\t" + "\'" + acvodip['lastname'] + "\'"

            acvodip['worktype'] = fieldsets[0].re("Work Type:\s+</div>\s+(\w+)\s+")[0].strip()
            print "Work type:\t" + "\'" + acvodip['worktype'] + "\'"
        except IndexError:
            print "Index error!!"

        # Parse addresses - loop through remaining fieldsets for addresses

        addresses = []
        for i in range(1, len(fieldsets), 1):
            address = {}

            name = fieldsets[i].re("Business/Organization Name[\s\d]*:\s*</div>\n(.*)</div>")
            address['name'] = name[0].strip() if len(name) > 0 else None

            street = fieldsets[i].re("Street[\s\d]*:\s*</div>\n(.*)</div>\s*")
            address['street'] = street[0].strip() if len(street) > 0 else None

            city = fieldsets[i].re("City[\s*\d*]*:\s*</div>\n(.*)</div>\s*")
            address['city'] = city[0].strip() if len(city) > 0 else None

            state = fieldsets[i].re("State[\s*\d*]*:\s*</div>\n(.*)</div>\s*")
            address['state'] = state[0].strip() if len(state) > 0 else None

            postalcode = fieldsets[i].re("Postal Code[\s*\d*]*:\s*</div>\n(.*)</div>\s*")
            address['postalcode'] = postalcode[0].strip() if len(postalcode) > 0 else None

            country = fieldsets[i].re("Country[\s*\d*]*:\s*</div>\n(.*)</div>\s*")
            address['country'] = country[0].strip() if len(country) > 0 else None

            addresses.append(address)

        acvodip['addresses'] = addresses
        # print "# Addresses:" + str(len(addresses)) + "\n"
        for a in acvodip['addresses']:
            print str(a)

        return acvodip

    def parse(self, response):
        response = response.replace(body=response.body.replace(
            '<br/>', '<br /')
        )
        return self._parse_response(response,
                                    self.parse_start_url,
                                    cb_kwargs={},
                                    follow=True)
