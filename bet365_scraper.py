from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import Proxy, ProxyType
from contextlib import suppress
from re import match
from time import sleep
import argparse
import random
import bet_parser

BET_365_INPLAY = "https://www.bet365.com/#/IP"
BET_365_SPORTS = "https://www.bet365.com/#/HO"
BET_365 = "https://www.bet365.com"
PROXY_PAGE = "https://free-proxy-list.net/"
PROXY_LIST = []
PROXY_USED = None
DRIVER_CAPABILITIES = None
driver = None

DRIVER_OPTIONS = Options()
USER_CONFIG = None


class UserOptions:
    """
    Stores the user's options
    """
    def __init__(self):
        self.use_proxy = False
        self.headless = True
        self.refresh = 3
        self.testing = False


class ProxyNode:
    """
    Stores the ip and port of a possible Proxy
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __repr__(self):
        return "{}:{}".format(self.ip, self.port)


def get_proxy_list():
    """
    Downloads a list of proxies
    :return updates a global variable, PROXY_LIST:
    """
    from requests import get as get_page
    global PROXY_LIST, PROXY_PAGE

    print("Downloading proxies...")
    proxy_page = get_page(PROXY_PAGE).text
    soup = BeautifulSoup(proxy_page, 'html.parser')
    table = soup.find_all('tr')
    for row in table:
        with suppress(IndexError):
            data = [x.string for x in row.find_all('td')]
            if match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", str(data[0])):
                PROXY_LIST.append(ProxyNode(str(data[0]), int(data[1])))
    print("Received {} proxies".format(len(PROXY_LIST)))


def set_chrome_proxy():
    global DRIVER_CAPABILITIES, PROXY_USED

    PROXY_USED = repr(random.choice(PROXY_LIST))
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = PROXY_USED
    #proxy.socks_proxy = PROXY
    proxy.ssl_proxy = PROXY_USED

    DRIVER_CAPABILITIES = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(DRIVER_CAPABILITIES)


def main():
    global driver
    print(f"using proxy {PROXY_USED}")

    driver = webdriver.Chrome("chromedriver.exe", chrome_options=DRIVER_OPTIONS, desired_capabilities=DRIVER_CAPABILITIES)

    driver.get(BET_365)

    while True:
        with suppress(Exception):
            driver.find_element_by_link_text("English").click()
            break

    print("Navigating to In-Plays...")
    while True:
        with suppress(Exception):
            left_menu_div = driver.find_elements_by_class_name("wn-WebNavModule")
            left_menu = left_menu_div[0].find_elements_by_class_name("wn-Classification")
            break
    for link in left_menu:
        if link.text.startswith("Live"):
            link.click()
            break

    print("Getting In-Plays...")
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "gl-Participant")))
    except TimeoutException:
        pass

    print("Parsing data...")
    global USER_CONFIG
    while True:
        html = driver.execute_script("return document.documentElement.outerHTML;")
        matches = bet_parser.parse_bet365(page=html)
        for m in matches:
            print(m)
        sleep(USER_CONFIG.refresh)


def handle_args():
    global USER_CONFIG

    USER_CONFIG = UserOptions()
    args = argparse.ArgumentParser(description="This script utilizes Selenium and BeautifulSoup in order to "
                                   "scrape real time data from bet365.com's Live In-Plays")
    args.add_argument("--no-headless", action='store_false',
                      help="Whether or not you want the Selenium browser to be visible. (default: True)")
    args.add_argument("-p", "--use-proxy", action='store_true',
                      help="Whether or not you want the script to use a list of free proxies."
                           "Warning: slows down performance.")
    args.add_argument("-r", "--refresh", default=3.0,
                      help="The amount of time the script waits in seconds between reading the contents of the website."
                            "(Default: 3 seconds)")
    args.add_argument("--testing", action='store_true',
                      help="Whether or not you're doing testing. If true, reads local bet365 page instead of opening"
                            " a Selenium instance.")

    args = args.parse_args()
    USER_CONFIG.headless = args.no_headless
    USER_CONFIG.use_proxy = args.use_proxy
    USER_CONFIG.refresh = args.refresh
    USER_CONFIG.testing = args.testing


if __name__ == "__main__":
    handle_args()

    if USER_CONFIG.use_proxy:
        get_proxy_list()
        set_chrome_proxy()

    DRIVER_OPTIONS.headless = USER_CONFIG.headless

    with suppress(Exception):
        try:
            if USER_CONFIG.testing:
                bet_parser.parse_bet365(bet_parser.RUN_EXAMPLE)
            else:
                main()
        finally:
            print("Closing driver.")
            driver.close()
