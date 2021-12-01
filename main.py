"""

TO RUN CODE FROM PYCHARM, TAP THE RUN BUTTON
TO RUN FROM TERMINAL, OPEN TERMINAL AND NAVIGATE TO THE DIRECTORY WHERE THE FILE IS STORED
EXAMPLE: C:\Users\JEANNOEL\PycharmProjects\craftbot
USE COMMAND : python main.py
YOU WILL BE REQUESTED TO ENTER THE ENDPOINT, EG TESLA, SLACK OR THE COMPANY NAME
THE FILE WILL BE SAVED WITH THE COMPANY NAME UNDER THE SAME DIRECTORY
IF SCRAPE FAILS, PLEASE RETRY 3-4 TIMES
ALSO, CHECK TO MAKE SURE THE COMPANY IS AVAILABLE

NB, WHEN YOU ADD AN ENDPOINT, IT IS APPENDED TO THE URL
EG IF YOU GIVE ENDPOINT AS tesla, THEN URL WILL BE craft.co/tesla
PROVIDE URL IN SMALL LETTERS


"""



import cloudscraper
from scrapy import Selector
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from details import get_details
import json
from time import sleep
DRIVER_PATH = 'C:/Users/JEANNOEL/Desktop/selenium/chromedriver.exe'

def get_chrom_driver():
    s = Service(DRIVER_PATH)
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # driver = webdriver.Chrome(options=options, service=s)

    browser = webdriver.Chrome(service=s)
    browser.get("https://craft.co/tesla")
    delay = 20  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'summary__company-name')))
        print("Page is ready!")

    except TimeoutException:
        print("Loading took too much time!")



    # s = Service('C:/Users/JEANNOEL/Desktop/selenium/chromedriver.exe')
    # browser = webdriver.Chrome(service=s)
    # url = 'https://craft.co/tesla'
    # browser.get(url)
    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "summary__company-name"))
    #     )
    # finally:
    #     driver.quit()
    print(myElem.page_source)

def fetch_html(endpoint):
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    return str(scraper.get(f"https://craft.co/{endpoint}").text.encode("utf-8"))

    # with open("myhtml.txt", "r") as f:
    #     text = f.read()
    #     # print(text)
    #     return str(text.encode("utf-8"))

def save_results(my_json, file_name):
    with open(f'{file_name}.json', 'w') as f:
        f.write(json.dumps(my_json))

    f.close()


def small_sleep(param):
    sleep(param)


if __name__ == '__main__':
    endpoint_text = input("enter company name eg. slack, tesla: -  ")
    body = fetch_html(endpoint_text)
    html = body
    response_text = Selector(text=html)
    website_details = get_details(response_text)

    save_results(website_details, endpoint_text)




    # get_chrom_driver()
    # i = 0
    # while True:
    #     i+=1
    #     try:  # returns a CloudScraper instance
    #         scraper = cloudscraper.create_scraper(delay=10)
    #         print(scraper.get("https://craft.co/tesla").text)
    #     except Exception as e:
    #         print(f"retying {i} {e}")
    #         pass

    # endpoint_text = input("please enter endpoint or company name eg tesla or slack or uber etc")
    # html = ""
    # counter = 0
    # while True:
    #     counter += 1
    #     if counter > 50:
    #         break
    #     try:
    #         body = fetch_html(endpoint_text)
    #         if body:
    #             html = body
    #             response_text = Selector(text=html)
    #             website_details = get_details(response_text)
    #
    #             save_results(website_details, endpoint_text)
    #             break
    #         small_sleep(.5)
    #     except:
    #         print(f"get failed- retrying {counter}")
