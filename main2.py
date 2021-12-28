import cloudscraper
from scrapy import Selector

from companies import my_json
from details import get_details
import json
from time import sleep
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path


def log_file_saved(file_name):
    print("*" * 20)
    print(f" file saved succesfully {file_name}")
    print("*" * 20)


def log_text(txt):
    print()
    print("*" * 20)
    print(str(txt))


def fetch_html(endpoint_url):
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    return str(scraper.get(endpoint_url).text.encode("utf-8"))


def str_encode(my_str):
    return urllib.parse.quote_plus(my_str)


def fetch_home_html(endpoint, should_locate=False):
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    home_url = f"https://craft.co/search?layout=list&order=size_desc&q={str_encode(endpoint)}"
    # there are many companies so add location
    if should_locate:
        log_text(f"fetching for location {comp_location}")
        home_url += f"&locations={str_encode(comp_location)}"
        print(home_url)
    else:
        log_text(f"FETCHING home html for {company_name}")
        print(home_url)
    return str(scraper.get(home_url).text.encode("utf-8"))


def save_results(save_json, file_name):
    with open(f'{file_name}-{company_name}.json', 'w') as f:
        f.write(json.dumps(save_json))
        log_file_saved(file_name)
    f.close()


def small_sleep(param):
    sleep(param)


def make_request(site_url):
    body = ""
    counter = 0
    while "summary__company-name" not in body:
        counter += 1
        try:
            # param is url of a particular website to fetch
            body = fetch_html(site_url)
        except:
            print(f"error in fetching {site_url} body")
            body = ""

        if "summary__company-name" in body:
            body = Selector(text=body)
            # get details for this website, return json of company details
            website_details = get_details(body, site_url)
            print(f"details for {company_name} gotten")
            return website_details
            # print(website_details)
            # break

        else:
            print(f"error, retrying {counter} of 50 times")

        if counter == 20:
            print("unable to scrape data, please try later")
            break
    return None


def get_home_location_companies(response):
    # first 5 homepage company cards
    cards = response.css("._2US_W")
    # if matched_name_cards list is empty, exit
    if not cards:
        log_text(f"no names match from locations {comp_location}")
        return
    # if only one card, fetch data, else fetch location
    if len(cards) >= 1:
        # get details, save and exit
        card_url = cards[0].css("._3egN7 ::attr(href)").get()
        website_details = make_request(f"https://craft.co{card_url}")
        save_results(website_details, endpoint_text)
        return
    # else make request to get location


def get_location_options():
    body = ""
    counter = 0
    while "_2US_W" not in body:
        counter += 1

        try:
            # to fetch the homepage containing the list of possible results
            # returns string of the page html
            body = fetch_home_html(endpoint_text, should_locate=True)
        except Exception:
            log_text(f"error in fetching home location for {company_name}")
            body = ""

        if "_2US_W" in body:
            body = Selector(text=body)
            # function to process the companies in the homepage
            get_home_location_companies(body)
            break

        else:
            print(f"error, retrying {counter} of 20 times")

        if counter == 20:
            print("unable to scrape data, please try later")
            break


def get_home_companies(response):
    # first 5 homepage company cards
    cards = response.css("._2US_W")
    # if matched_name_cards list is empty, exit
    if not cards:
        log_text(f"no names found for {company_name}")
        return
    # if only one card, fetch data, else fetch location
    if len(cards) == 1:
        # get details, save and exit
        card_url = cards[0].css("._3egN7 ::attr(href)").get()
        website_details = make_request(f"https://craft.co{card_url}")
        save_results(website_details, endpoint_text)
        return
    # else make request to get location

    if len(cards) > 1:
        log_text(f"more than one compant so fetching location {comp_location}")
        get_location_options()


def get_options():
    body = ""
    counter = 0
    while "_2US_W" not in body:
        counter += 1

        try:
            # to fetch the homepage containing the list of possible results
            # returns string of the page html
            body = fetch_home_html(endpoint_text)
        except Exception:
            # print("error in fetching home body")
            body = ""

        if "_2US_W" in body:
            body = Selector(text=body)
            # function to process the companies in the homepage
            get_home_companies(body)
            break

        else:
            print(f"error, retrying {counter} of 20 times")

        if counter == 20:
            print(f"unable to scrape data for {company_name}, please try later")
            break


if __name__ == '__main__':
    # endpoint_text = input("enter company name eg. slack, tesla: -  ")
    for ind, company in enumerate(my_json):
        # url = endpoint_text = ""
        url = company.get("url", None)
        endpoint_text = company_name = company.get("company", None)
        if endpoint_text is None:
            log_text("No company name")
            continue
        comp_location = company.get("location")
        log_text(f"fetching {company_name}")
        get_options()
        sleep(2)

        log_text(f"FETCHING NEXT COMPANY {ind}")
