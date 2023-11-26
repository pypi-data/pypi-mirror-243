import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def tor_driver():
    proxy = "socks5://localhost:9050"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server=%s" % proxy)
    driver = webdriver.Chrome(options=options)
    return driver


def trequests(url, verify=True):
    proxies = {
        "http": "socks5h://localhost:9050",
        "https": "socks5h://localhost:9050",
    }
    return requests.get(url, proxies=proxies, verify=verify)
