from urllib.request import Request

import cfscrape
import cloudscraper
import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser


class CraftbotSpider(scrapy.Spider):
    name = 'craftbot'
    # allowed_domains = ['x']
    start_urls = ['https://google.com']



    def parse(self, response):
        scraper = cloudscraper.create_scraper()
        body = scraper.get("https://craft.co/tesla").text
        response = Selector(text=body)
        print(response.text)

process = CrawlerProcess()
process.crawl(CraftbotSpider)
process.start()
