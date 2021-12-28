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

from companies import my_json
from details import get_details
import json
from time import sleep

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path


# DRIVER_PATH = 'C:/Users/JEANNOEL/Desktop/selenium/chromedriver.exe'
# You can use this as a class to store all common functions and data for all our scrapers
# Just say that every scraper inherits from this scraper, like I did in the linkedin.py file
# ideally after we are done with the scraper scripts we can use this guy to dictate which
# scraper will run and rotate IP's
class Dbconnect():
    def __init__(self):
        print("in init")
        env_file = os.path.join(Path(__file__).parent.parent.parent, ".env")
        load_dotenv(env_file)
        self.mongo_address = os.getenv("MONGO_REMOTE")
        print(self.mongo_address)
        print("init ended")

    def __enter__(self):
        print("in enter")
        self.mongo_client = MongoClient(self.mongo_address)
        print("enter ended")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("in exit")
        self.mongo_client.close()
        print("exit ended")

    def SaveData(self, data):
        if self.mongo_client.assignments.Craft.find({"id": data['id']}).count() > 0:
            print(f"Record already exists")
            self.mongo_client.assignments.Craft.update_one({'id': data['id']}, {'$set': data})
            print("Record Updated.." + str(data['title']))

        else:
            self.mongo_client.assignments.Craft.insert_one(data)
            print("New Record Inserted " + str(data['title']))

    def GetAll(self):
        return list(self.mongo_client.assignments.Craft.find())

    def UpdateData(self, data, id):
        if self.mongo_client.assignments.Craft.find({"id": id}).count() > 0:
            print(f"Record already exists")
            self.mongo_client.assignments.Craft.update_one({'id': id}, {'$set': data})
            print(f"Record Updated Successfully..")


def log_file_saved(file_name):
    print("*"*20)
    print(f" file saved succesfully {file_name}")
    print("*" * 20)

def fetch_html(endpoint_url):
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # url = f"https://craft.co{endpoint}"
    return str(scraper.get(endpoint_url).text.encode("utf-8"))


def fetch_home_html(endpoint):
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    home_url = f"https://craft.co/search?layout=list&order=size_desc&q={endpoint}"
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
            print("details gotten")
            return website_details
            # print(website_details)
            # break

        else:
            print(f"error, retrying {counter} of 50 times")

        if counter == 51:
            print("unable to scrape data, please try later")
            break
    return None


def get_home_companies(response):
    # first 5 homepage company cards
    cards = response.css("._2US_W")[:5]
    # check for the cards that the names match
    matched_name_cards = [card for card in cards if company_name == card.css("h3._35_BY::text").get()]
    # if matched_name_cards list is empty, exit
    if not matched_name_cards:
        print("no names match from homepage")
        return

    # if there is only one card, get the details
    if len(matched_name_cards) == 1:
        # get details, save and exit
        card_url = matched_name_cards[0].css("._3egN7 ::attr(href)").get()
        website_details = make_request(f"https://craft.co{card_url}")
        save_results(website_details, endpoint_text)
        print("ond company found and saved")
        return
    # loop through cards with matched names and compare url and location
    for card in matched_name_cards:
        card_url = card.css("._3egN7 ::attr(href)").get()
        print(f"fetching card for url {card_url}")


        # getting details for the card, returns json
        website_details = make_request(f"https://craft.co{card_url}")

        if website_details is not None:
            # check if websites match
            if website_details["Website"].strip().replace(" ", "") == url.strip().replace(" ", ""):
                # url match
                # print(website_details)
                save_results(website_details, endpoint_text)
                # with Dbconnect() as client:
                #     client.SaveData(website_details)
                print(f"complete: file saved as {endpoint_text} - {company_name}")
                return  # exit function

            # check if company locations match
            if website_details["HQ"].strip().replace(" ", "") == comp_location.strip().replace(" ", ""):
                save_results(website_details, endpoint_text)
                # url does not match,
                print(f"complete: file saved as {endpoint_text} - {company_name}")
                return
        else:
            print("website details is none,")
    # urls do not match, now check names


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
            print("error in fetching home body")
            body = ""

        if "_2US_W" in body:
            body = Selector(text=body)
            # function to process the companies in the homepage
            get_home_companies(body)
            break

        else:
            print(f"error, retrying {counter} of 50 times")

        if counter == 51:
            print("unable to scrape data, please try later")
            break


if __name__ == '__main__':
    # endpoint_text = input("enter company name eg. slack, tesla: -  ")
    for company in my_json:
        url = endpoint_text = ""
        try:
            url = company["url"]
        except KeyError:
            print("skipping because of no key url in " + str(company["company"]))

        try:
            endpoint_text = company_name = company["company"]
        except KeyError:
            print("skipping because of no key company name " + str(company["company"]))

        try:
            comp_location = company["location"]
        except KeyError:
            print("skipping because of no key location in " + str(company["company"]))

        get_options()
