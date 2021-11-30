def get_details(response):
    response.css("")
    my_json = {}
    try:
        my_json['company_name'] = response.css("h1.summary__company-name::text").get()
    except:
        my_json['company_name'] = "NA"

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
        pass

    try:
        my_json['company_summary'] = response.css("div.summary__description div ::text").get()
    except:
        my_json['company_summary'] = "NA"

    try:
        my_json['company_tags'] = ", ".join(response.css("ul.summary__tags > li.summary__tag a.craft-tag::text").getall())
    except:
        my_json['company_tags'] = "NA"

    try:
        my_table = response.css("table.summary__overview-table > tbody tr.summary__overview-table-row")
        for table_row in my_table:
            table_title = table_row.css("td.summary__overview-table-label-cell::text").get()

            if table_title == "Website":
                table_value = table_row.css("td.summary__overview-table-content-cell a.craft-link::text").get()

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
        pass

    try:
        company_name = response.css("")
    except:
        pass

    try:
        company_name = response.css("")
    except:
        pass
