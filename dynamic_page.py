# ////////////////////////////////////////////////////////////// #
# PARSING https://realpython.com/                                #
# THE TASK IS TO GET EVERY ARTICLE INSIDE 'NEW RELEASES' SECTION #
# AND EXTRACT TITLE, LINK AND TAGS FROM PREVIEW                  #
# ////////////////////////////////////////////////////////////// #
import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        "authority": "www.google-analytics.com",
        "method": "POST",
        "path": "/j/collect?v=1&_v=j96&a=2065656292&t=pageview&_s=1&dl=https%3A%2F%2Frealpython.com%2F&ul=ru-ru&de=UTF-8&dt=Python%20Tutorials%20%E2%80%93%20Real%20Python&sd=24-bit&sr=1536x864&vp=366x714&je=0&_u=QACAAEABAAAAAC~&jid=516262858&gjid=1364967528&cid=1133214904.1650799092&tid=UA-35184939-1&_gid=1284672569.1655909720&_r=1&_slc=1&cd1=1&cd2=0&z=1957463574",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-length": "0",
        "content-type": "text/plain",
        "origin": "https://realpython.com",
        "referer": "https://realpython.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    }
    req = requests.get(url, headers)

    with open("raw_pages/dynamic_page.html", "w", encoding="utf-8") as file:
        file.write(req.text)


get_data("https://realpython.com/")
