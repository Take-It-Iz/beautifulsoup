# ////////////////////////////////////////////////////// #
# PARSING LAPTOPS PAGE ON https://rozetka.com.ua/ AND    #
# RETRIEVING LAPTOP TITLE, PRICE AND LINK                #
# THE RESULT DATA HAS TO BE STORED IN JSON AND CSV FILES #
# ////////////////////////////////////////////////////// #

import os
import requests
from bs4 import BeautifulSoup as bs
import re
import json
import csv
from operator import itemgetter
from random import randint
from time import sleep


##################################################################################
# THIS CODE SECTION IS NOT NECESSARY TO RUN AFTER THE DATA IS COLLECTED          #
# THE CODE WILL BE UNCOMMENTED IN THE FINAL GIT COMMIT FOR READING EASE PURPOSE  #
##################################################################################

# define search filter
gpu_series = "seriya-diskretnoi-videokarti=geforce-rtx-3060"
# headers are used for crawler to immitate real user activity
headers = {
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
}
url = f"https://rozetka.com.ua/notebooks/c80004/{gpu_series}"
results = requests.get(url, headers=headers).text
doc = bs(results, "lxml")

pages_elements = doc.select(
    "a.pagination__link.ng-star-inserted"
)  # search for a tag that matches 2 CSS-classes (here - page number button)
"""
contents[0] means the first element inside the tag,
because the tag itself contains 'traps' - invisible comments that look like <!----->
to catch web-scrapers
"""
pages = [int(p.contents[0]) for p in pages_elements]

# check if file exists and delete if exists
if os.path.exists("raw_pages/rozetka_laptops_raw.html"):
    os.remove("raw_pages/rozetka_laptops_raw.html")

# sleep after the initial request to avoid server loading
sleep(randint(2, 10))

# save every html-page to the common file to further scrape the data
with open("raw_pages/rozetka_laptops_raw.html", "a+", encoding="utf-8") as file:
    file.seek(0)  # move read cursor to the start of file
    if len(file.readlines()) > 0:  # if file is not empty - append '\n'
        file.write("\n")

    # loop through every page and scrape the raw data
    for page in range(1, len(pages) + 1):
        url = f"https://rozetka.com.ua/notebooks/c80004/page={page};{gpu_series}"
        results = requests.get(url).text
        file.write(results)
##################################################################################
#                               END OF SECTION                                   #
##################################################################################


with open("raw_pages/rozetka_laptops_raw.html", encoding="utf-8") as file:
    src = file.read()

doc = bs(src, "lxml")

divs = doc.find_all(class_="goods-tile__inner")  # collect all product element blocks
"""
list of dictionaries that contains scraped products
(each element is a separate dict with "Title", "Price" and "Link" pairs)
"""
products_found_unsorted = []

# loop through every element and scrape the data
for d in divs:
    product_link_tag = d.find(
        "a", {"class": "goods-tile__heading ng-star-inserted"}
    )  # find an 'a' tag of a product
    product_link_value = product_link_tag.get("href")  # extract the product link
    product_title = product_link_tag.get("title")  # the title is duplocated in the link
    product_price_tag = d.find("span", {"class": "goods-tile__price-value"})
    """
    regex is to remove all spaces in string including invisible ones;
    products may not have price element in the container, so we have to check if this element
    is null (None)
    """
    product_price_value = (
        int(re.sub(r"\s+", "", product_price_tag.text, flags=re.UNICODE))
        if product_price_tag is not None
        else 0
    )

    products_found_unsorted.append(
        {
            "Title": product_title,
            "Price": product_price_value,
            "Link": product_link_value,
        }
    )

# sort the list by "Price" from the most expensive to the cheapest
products_found_sorted = sorted(
    products_found_unsorted, key=itemgetter("Price"), reverse=True
)
for p in products_found_sorted:
    print(
        "Title : "
        + p["Title"]
        + "\nPrice : "
        + str(p["Price"])
        + "\nLink : "
        + p["Link"]
        + 3 * "\n"
    )

# save to json
with open("json/rozetka_laptops.json", "w", encoding="utf-8") as file:
    json.dump(products_found_unsorted, file, indent=4, ensure_ascii=False)


# save to csv
with open("csv/rozetka_laptops.csv", "w", encoding="utf-8") as file:
    products_headers = products_found_unsorted[0].keys()
    writer = csv.DictWriter(file, fieldnames=products_headers)

    writer.writeheader()
    writer.writerows(products_found_unsorted)
