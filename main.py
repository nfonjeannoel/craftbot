import cloudscraper
from scrapy import Selector

from details import get_details


def fetch_html():
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    return str(scraper.get("https://craft.co/tesla").text.encode("utf-8"))

#
# def save_html(html):
#     with open("myhtml.txt", "w") as f:
#         f.write(body)




if __name__ == '__main__':
    html = ""
    while True:
        try:
            body = fetch_html()
            if "!DOCTYPE" in body.split()[0]:
                html = body
                # save_html(body)
                break
        except:
            print("get failed- retrying")

    response_text = Selector(text=html)
    # print(response.css("#__next > div > div.layout-container > div > div > div.summary > div.summary__middle-row > div:nth-child(1) > div > ul > li:nth-child(1) > a::text").get())
    get_details(response_text)
# while body.split()[-1] == "version." or body.split()[-1] == "version.":

# print(body)
# with open("myhtml.txt", "w") as f:
#     f.write(str(body))
#
#
# with open("myhtml.txt") as f:
#     file = f.read()
#     print("file saved")
# response = Selector(text=file)
# print(response.css("#__next > div > div.layout-container > div > div > div.summary > div.summary__middle-row > div:nth-child(1) > div > ul > li:nth-child(1) > a::text").get())

