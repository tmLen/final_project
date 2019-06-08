from random import choice
import json
import re
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from urllib import request as urlrequest
import requests

import settings
from utils import get_soup_selenium, json_to_file, get_proxy


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

#функция получает url сайта запускает selenium driver, кликает на ссылку и возвращает страницу на которую перешли по ссылке
def get_html_selenium_with_click(url):
    # try:

        #прокси для селениума
        webdriver.DesiredCapabilities.FIREFOX['proxy']={
            "httpProxy":get_proxy('http'),
            "ftpProxy":get_proxy('http'),
            "sslProxy":get_proxy('ssl'),
            # "noProxy":None,
            "proxyType":"MANUAL"
                    }
        driver = webdriver.Firefox()
        driver.get(url)
        driver.find_element_by_link_text('').click()

        result = driver.page_source
        driver.close()
        return(result)
    # except(common.exceptions.WebDriverException):
    #     return False

def get_stations_href(regions):
    stations = []
    for region in regions:
        url = f"{settings.SRC[2]}/{region}"
        print(url)
        # soup = get_soup_selenium(url)
        # links = 

if __name__ == '__main__':

    #прокси для requests
    # with open('proxy_http_ip.txt', 'r') as fin:
    #     proxy_list = [x.replace('\n', '') for x in fin.readlines()]
    # url = 'http://www.benzin-price.ru'
    # proxies = {'http': choice(proxy_list)}
    # reque = requests.get(url, proxies=proxies)


    # with open('data/bf_regions_hrefs.json', 'r') as fin:
    #     regions_data = json.load(fin)
    # get_stations_href(regions_data)

    
    print(get_html_selenium_with_click('https://mimobaka.ru'))

    
    
