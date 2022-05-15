import requests
from bs4 import BeautifulSoup as bs
import re
from operator import itemgetter

# define search filter
gpu_series = "seriya-diskretnoi-videokarti=geforce-rtx-3060"

"""initial request with filter(s)
in this example there's only one filter to try parsing multiple pages"""
url = f"https://rozetka.com.ua/notebooks/c80004/{gpu_series}"
results = requests.get(url).text
doc = bs(results, "lxml")

pages_elements = doc.select(
    "a.pagination__link.ng-star-inserted"
)  # search for a tag that matches 2 CSS-classes (here - page number button)
"""contents[0] means the first element inside the tag,
because the tag itself contains 'traps' - invisible comments that look like <!----->
to catch web-scrapers"""
pages = [int(p.contents[0]) for p in pages_elements]

"""list of dictionaries that contains scraped products
(each element is a separate dict with "Title", "Price" and "Link" pairs)"""
products_found_unsorted = []

# loop through every page and scrape the data
for page in range(1, len(pages) + 1):
    url = f"https://rozetka.com.ua/notebooks/c80004/page={page};{gpu_series}"
    results = requests.get(url).text
    doc = bs(results, "lxml")

    # collect all product element blocks
    divs = doc.find_all(class_="goods-tile__inner")

    # loop through every element and scrape the data
    for d in divs:
        product_link_tag = d.find(
            "a", {"class": "goods-tile__heading ng-star-inserted"}
        )  # find 'a' tag for a product
        product_link_value = product_link_tag.get("href")  # extract the product link
        product_title = product_link_tag.get(
            "title"
        )  # the title is duplocated in the link
        product_price_tag = d.find("span", {"class": "goods-tile__price-value"})

        """regex is to remove all spaces in string including invisible ones;
        products may not have price element in the container, so we have to check if this element 
        is null (None)"""
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
