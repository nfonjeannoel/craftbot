from scrapy import Selector

with open("myhtml.txt") as f:
    file = f.read()
response = Selector(text=file)

my_table = response.css("table.summary__overview-table > tbody tr.summary__overview-table-row")
for table_row in my_table:
    table_title = table_row.css("td.summary__overview-table-label-cell::text").get()

    if table_title == "Website":
        table_value = table_row.css("td.summary__overview-table-content-cell a.craft-link::text").get()
    elif table_title == "Employee Ratings":
        table_value = table_row.css("td.summary__overview-table-content-cell > span > span:nth-child(2)::text").get()

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

    # print(f"{table_title} - {table_value}")