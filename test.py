from scrapy import Selector

with open("myhtml.txt") as f:
    file = f.read()
response = Selector(text=file)

office_locations = response.css("div.cp-locations__list-block")
for location in office_locations:
    location_name = location.css("div.cp-locations__list-title > span::text").get()
    address = location.css("div.cp-locations__list-address::text").get()



    print(f"{location_name} - {address} ")