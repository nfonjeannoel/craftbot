import json
from urllib.parse import urljoin

import cloudscraper

# scraper = cloudscraper.create_scraper()
# url = "https://craft.co/search?layout=list&order=relevance&q=mit"
# data = scraper.get(url).text
# print(data)
# from scrapy import Selector
#
# with open("test.txt", "r") as f:
#     response = f.read()
# # print(response)
# response = Selector(text=response)
#
# cards = response.css("._2US_W")
# for card in cards:
#     url = card.css("._3egN7 ::attr(href)").get()
#     print(url)
# with open("companies.txt", "r") as f:
#     myjson = f.read()
#     myjson = json.loads(myjson)
#     print(type(myjson))
import urllib.parse
safe_string = urllib.parse.quote_plus("hey there, i am good")
print(safe_string)