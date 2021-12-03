# """
#
# FROM TERMINAL INSTALL MODULE cloudscraper WITH pip install cloudscraper
# TO RUN CODE FROM PYCHARM, TAP THE RUN BUTTON
# TO RUN FROM TERMINAL, OPEN TERMINAL AND NAVIGATE TO THE DIRECTORY WHERE THE FILE IS STORED
# EXAMPLE: C:\Users\JEANNOEL\PycharmProjects\craftbot
# USE COMMAND : python main.py
# YOU WILL BE REQUESTED TO ENTER THE ENDPOINT, EG TESLA, SLACK OR THE COMPANY NAME
# THE FILE WILL BE SAVED WITH THE COMPANY NAME UNDER THE SAME DIRECTORY
# IF SCRAPE FAILS, PLEASE RETRY 3-4 TIMES
# ALSO, CHECK TO MAKE SURE THE COMPANY IS AVAILABLE
#
# NB, WHEN YOU ADD AN ENDPOINT, IT IS APPENDED TO THE URL
# EG IF YOU GIVE ENDPOINT AS tesla, THEN URL WILL BE craft.co/tesla
# PROVIDE URL IN SMALL LETTERS
#
#
# """
# comment

import cloudscraper
from scrapy import Selector
from details import get_details
import json
from time import sleep

DRIVER_PATH = 'C:/Users/JEANNOEL/Desktop/selenium/chromedriver.exe'


def fetch_html(endpoint):
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    url = f"https://craft.co/{endpoint}"
    return str(scraper.get(url).text.encode("utf-8")), url


def save_results(my_json, file_name):
    with open(f'{file_name}.json', 'w') as f:
        f.write(json.dumps(my_json))

    f.close()


def small_sleep(param):
    sleep(param)


if __name__ == '__main__':
    endpoint_text = input("enter company name eg. slack, tesla: -  ")
    body = ""
    counter = 0
    website_details = ""
    while "summary__company-name" not in body:
        counter += 1

        try:
            body, page_url = fetch_html(endpoint_text)
        except:
            print("error in fetching body")
            body = ""

        if "summary__company-name" in body:
            body = Selector(text=body)
            website_details = get_details(body, page_url)
            print(website_details)
            save_results(website_details, endpoint_text)
            print(f"complete: file saved as {endpoint_text}")
            break

        else:
            print(f"error, retrying {counter} of 50 times")

        if counter == 51:
            print("unable to scrape data, please try later")
            break