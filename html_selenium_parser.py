from bs4 import BeautifulSoup
from random import choice
import json
import re
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from urllib import request as urlrequest

import proxy
import settings
from utils import get_soup_selenium, json_to_file


#Собираем данные о регионах с сайта. возвращает массив ссылок на страницы регионов 
def get_regions_href(url):
    region_hrefs = []
    soup = get_soup_selenium(url)
    links = soup.findAll('a', {"href": re.compile(r'zapravka\.php\?region*')})
    for link in links:
        region_hrefs.append(link['href'])
    return region_hrefs

#сохраняем данные о регионах в файл
def save_regions_href():
    regions_hrefs = get_regions_href(settings.SRC[1])
    json_to_file(regions_hrefs,'data/bf_regions_hrefs.json')

def get_stations_hrefs(driver, stations):
    pass

#функция получает url сайта запускает selenium driver, кликает на ссылку и возвращает страницу на которую перешли по ссылке
def get_stations_data(url, proxy, stations_hrefs):
    try:
        cur_proxy = proxy.get_active_proxy()
    except (ValueError):
        return False
    try:
        #прокси для селениума
        webdriver.DesiredCapabilities.FIREFOX['proxy']={
            "httpProxy":f"{cur_proxy}:{proxy.get_proxy_port('http')}",
            "sslProxy":f"{cur_proxy}:{proxy.get_proxy_port('ssl')}",
            "proxyType":"MANUAL"
                    }
        
        driver = webdriver.Firefox()
        driver.get(url)
        get_stations_hrefs(driver.find_element_by_link_text('Весь список').click(), stations_hrefs)

        result = driver.page_source
        driver.close()
        return(result)
    except(common.exceptions.WebDriverException):
        proxy.ban_proxy(cur_proxy)


def get_stations(regions, proxy):
    stations = []
    for region in regions:
        url = f"{settings.SRC[2]}/{region}"
        get_stations_data(url, proxy, stations)
    return stations

if __name__ == '__main__':
    p = ProxiesQueue()
    with open('data/bf_regions_hrefs.json', 'r') as fin:
        regions_data = json.load(fin)
    get_stations(regions_data, p)
