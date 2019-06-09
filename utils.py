from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json
from random import choice
import requests
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
import time


#Принимает строку, возвращает число, если не может конвертировать возвращает False
def int_checker(str):
    try:
        return int(str)
    except (ValueError):
        return False

#Принимает структуру и адрес куда нужно записать json с этой структурой
def json_to_file(data, path):
    with open(path, 'w') as fout:
        json.dump(data, fout, ensure_ascii=False, sort_keys=True)

#функция получает url сайта, делает GET запрос и возвращает текст страницы, а если не удалось его получить - False
def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False

#функция получает url сайта и открывает сайт через селениум 
def get_html_selenium(url):
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        result = driver.page_source
        driver.close()
        return(result)
    except(common.exceptions.WebDriverException):
        return False

#функция принимает на вход текст страницы и возвращает объект BeautifulSoup
def get_soup(url):
    html_text = get_html(url)
    if html_text:
        return BeautifulSoup(html_text, 'html.parser')
    return False

def get_soup_selenium(url):
    html_text = get_html_selenium(url)
    if html_text:
        return BeautifulSoup(html_text, 'html.parser')
    return False

#функция создания url региона, на вход подается структура региона
def create_region_path(url, region, page_number):
    return url + region['href'] + 'page' + str(page_number)

#маппинг русских месяцов на номер месяца, на вход принимает строку ищет в ней название месяца и заменяет его на номер месяца
def date_translate(date_last_updated):
    translate_monthes = {'января':'01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля':'07', 'августа':'08', 'сентября':'09','октября':'10','ноября':'11','декабря':'12'}
    if date_last_updated.split()[1] in translate_monthes:
        return date_last_updated.replace(date_last_updated.split()[1], translate_monthes[date_last_updated.split()[1]])
    return date_last_updated

#возвращает строку с описанием разницы между двумя таймстемпами
def calc_duration(tmstmp1, tmstmp2):
    return str((tmstmp2-tmstmp1)//60) + ' мин ' + str((tmstmp2 - tmstmp1)%60 / 100 * 60) + ' сек '

#возвращает случайную проксю из списка
def get_proxy(type):
    with open('proxy_http_ip.txt', 'r') as fin:
        proxy_list = [x.split(':')[0] for x in fin.readlines()]
    if type == 'http':
        return f"{choice(proxy_list)}:8085"
    if type == 'socks':
        return f"{choice(proxy_list)}:1085"
    if type == 'ssl':
        return f"{choice(proxy_list)}:8085"
    return False

#функция возвращает текущеий таймстемп utc
def get_current_utc_timestamp():
    return int(datetime.utcnow().timestamp())

#функция возвращает дату из таймстемпа
def timestamp_to_date(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')