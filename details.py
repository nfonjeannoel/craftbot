def get_details(response, url):
    my_json = {'page_url': url, "Website": "", "HQ": ""}

    # initialise must use variables
    try:
        x = my_json['company_name'] = response.css("h1.summary__company-name::text").get()
        if x is None:
            my_json['company_name'] = response.css("h1.cp-summary__company-name::text").get()
            x = None
    except:
        my_json['company_name'] = "NA"
        print("error with company nam,e")
    # f
    try:
        matrices = response.css(".summary__top-metric-link")
        for matrix in matrices:
            matrix_title = matrix.css("span.summary__top-metric-title::text").get()
            matrix_value = matrix.css("span.summary__top-metric-bottom span.summary__top-metric-value::text").get()
            matrix_period = matrix.css("span.summary__top-metric-bottom span.summary__top-metric-period::text").get()
            my_json[matrix_title] = {
                'matrix_value': matrix_value,
                'matrix_period': matrix_period
            }

    except:
        print("error with matrices")
        pass

    try:
        x = my_json['company_summary'] = response.css("div.summary__description div ::text").get()
        if x is None:
            my_json['company_summary'] = " ".join(response.css("p::text").getall())
            x = None
    except:
        my_json['company_summary'] = "NA"

    try:
        x = my_json['company_industry'] = ", ".join(
            response.css("ul.summary__tags > li.summary__tag a.craft-tag::text").getall())

        if len(x) < 3:
            my_json['company_industry'] = ", ".join(
                response.css(".cp-summary__tag::text").getall())
            x = None
    except:
        my_json['company_industry'] = "NA"

    try:
        my_table = response.css("table.summary__overview-table > tbody tr.summary__overview-table-row")
        for table_row in my_table:
            table_title = table_row.css("td.summary__overview-table-label-cell::text").get()

            if "Website" in table_title:
                table_value = table_row.css(".summary__overview-table-content-cell > a::attr(href)").get()

            # elif table_title == "HQ":
            #     table_title = "Head Quarters"

            elif table_title == "Employee Ratings":
                table_value = table_row.css(
                    "td.summary__overview-table-content-cell > span > span:nth-child(2)::text").get()

            elif table_title == "Overall Culture":
                table_value = table_row.css("td.summary__overview-table-content-cell span.grade-badge::text").get()

            elif table_title == "Job Openings":
                table_value = table_row.css("td.summary__overview-table-content-cell a.craft-link::text").get()

            elif "Revenue" in table_title:
                table_value = table_row.css("td.summary__overview-table-content-cell a.craft-link::text").get()

            elif "Share Price" in table_title:
                table_value = table_row.css("td.summary__overview-table-content-cell a.craft-link::text").get()

            elif "Cybersecurity" in table_title:
                table_value = table_row.css("td.summary__overview-table-content-cell span.grade-badge::text").get()

            else:
                table_value = table_row.css("td.summary__overview-table-content-cell::text").get()

            my_json[table_title] = table_value
    except:
        print("error with my_table")
        pass

    try:
        social_links = response.css("li.craft-social-links__item")[:5]
        socials = {}
        for link in social_links:
            social_media = link.css("a.craft-social-links__link::attr(href)").get().split(".")[1]
            if "/" in social_media:
                social_media = link.css("a.craft-social-links__link::attr(href)").get().split("/")[-2].split(".")[0]

            social_media_url = link.css(" a.craft-social-links__link::attr(href)").get()

            socials[social_media] = social_media_url
        my_json["social_links"] = socials
    except:
        print("error with social_links")
        pass

    try:
        key_people = response.css("div.key-people__item")
        key_people_lst = []
        for person in key_people:
            person_name = person.css("div.key-people__info > h3.key-people__name::text").get()
            person_position = person.css("div.key-people__info > div.key-people__position::text").get()
            person_social_media = person.css(
                "div.key-people__info > div.key-people__social-links a.key-people__social-link::attr(href)").get()
            person_photo = person.css("div.key-people__picture-container img.key-people__picture::attr(src)").get()

            key_people_lst.append({
                "name": person_name,
                "position": person_position,
                "social_media": person_social_media,
                "photo": person_photo
            })

        my_json['key_people'] = key_people_lst
    except:
        print("error with key_people")
        pass

    try:
        office_locations = response.css("div.cp-locations__list-block")
        locations = []
        for location in office_locations:
            location_name = location.css("div.cp-locations__list-title > span::text").get()
            address = location.css("div.cp-locations__list-address::text").get()
            locations.append({
                "location_name": location_name,
                "location_address": address
            })

        my_json['office_locations'] = locations
    except:
        print("error with office_locations")
        pass

    return my_json
