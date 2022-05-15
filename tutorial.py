"""
some basics of parsing with BeautifulSoup with
notes about methods and workflow

pip install beautifulsoup
pip install --upgrade --force-reinstall beautifulsoup4
the best option is to install in the currently selected/virtual environment
pip install requests
pip install lxml
"""
import requests
from bs4 import BeautifulSoup as bs
import re

########## SEARCHING AND FILTERING ##########
##### scraping data from ROZETKA shop
#
# all Apple laptops
# url = "https://rozetka.com.ua/notebooks/c80004/producer=apple/"
# results = requests.get(url)
# print(results.text) # print raw result data
# doc = bs(results.text, "lxml")  # parse the result data with a parser
# print(doc.prettify())  # prettify is used to make data look structured

##### get price of a specific laptop model
# url = (
#     "https://rozetka.com.ua/apple_macbook_pro_16_m1_max_1tb_2021_space_gray/p322714708/"
# )
# results = requests.get(url)
# doc = bs(results.text, "lxml")
#
##### search for prices by element css class name
# prices = doc.find_all(
#     class_="product-prices__big product-prices__big_color_red"
# ) # returns a list
# print(prices[0].text)
#
##### return price element's parent container and extract data from it;
##### prices returns a list of prices, even if we search one element
# prices = doc.find_all(text="₴") # returns two currency characters instead of the price
# parent = prices[0].parent  # move to the parent of the first element
# print(parent)


##### scraping data from beautifulsoup tutorial on realpython.com
# url = "https://realpython.com/beautiful-soup-web-scraper-python/"
# results = requests.get(url)
# doc = bs(results.text, "lxml")
#
##### find the first 'div' tag
# div_tag = doc.find("div")
# print(div_tag.attrs)  # print list of tag's attributes
# print(div_tag["class"])  # print value of the specific element attribute inside the tag
#
##### find multiple tags
# multiple_tags = doc.find_all(
#     ["div", "p", "ul"]
# )  # find all selected tags with their content
# print(multiple_tags)
#
##### search by attribute value of a tag
# multiple_tags = doc.find_all(["a"], class_="dropdown-item")
# print(multiple_tags)
#
##### search by multiple attribute values of a tag
# multiple_tags = doc.find_all(["a"], class_="dropdown-item", text="Python Newsletter")
# print(multiple_tags)
#
##### search using regular expressions
# multiple_tags = doc.find_all(
#     text=re.compile("(s|S)crap")
# )  # tip: avoid '\' in the beginning of the regex sequence, if you're searching plain text
# for tag in multiple_tags:
#     print("\n" + 5 * "/" + tag.text)
#
##### limit the amount of search results
# multiple_tags = doc.find_all(text=re.compile("(s|S)crap"), limit=5)
# for tag in multiple_tags:
#     print("\n" + 5 * "/" + tag.text)


##### NAVIGATING THE HTML TREE #####
##### scraping data from beautifulsoup tutorial on realpython.com
# url = "https://realpython.com/beautiful-soup-web-scraper-python/"
# results = requests.get(url)
# doc = bs(results.text, "lxml")

# lists_collection = doc.ul  # collect all lists ('ul' tags content)
# lists_elements = lists_collection.contents  # collection of list content

# print(lists_elements[0].next_sibling)  # print the first element
# print(lists_elements[1].previous_sibling)  # print the previous element
# print(
#     lists_elements[0].next_siblings
# )  # all list elements after this one; returns generator object (iteratable)
# print(list(lists_elements[0].next_siblings))
# print(lists_elements[0].parent.name)  # print the parent tag name
