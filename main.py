import cloudscraper
from scrapy import Selector

from details import get_details
import json


def fetch_html(endpoint):
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    return str(scraper.get(f"https://craft.co/{endpoint}").text.encode("utf-8"))


def save_results(my_json, file_name):
    with open(f'{file_name}.json', 'w') as f:
        f.write(json.dumps(my_json))

    f.close()


if __name__ == '__main__':
    endpoint_text = input("please enter endpoint or company name eg tesla or slack or uber etc")
    html = ""
    counter = 0
    while True:
        counter += 1
        if counter > 50:
            break
        try:
            body = fetch_html(endpoint_text)
            if endpoint_text in body:
                html = body
                response_text = Selector(text=html)
                website_details = get_details(response_text)

                save_results(website_details, endpoint_text)
                break
        except:
            print(f"get failed- retrying {counter}")

