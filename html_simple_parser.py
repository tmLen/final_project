import time
import datetime
import settings
from utils import get_soup, json_to_file, int_checker, create_region_path, date_translate, calc_duration

#Функции ниже релевантны только для сайта mimobaka ¯\_(ツ)_/¯
#Если на вход подать другой сайт, то функции надо переписать

#функция получает ulr сайта и ищет на нем субъекты РФ в которых есть АЗС, возвращает словарь с данными 
def find_regions(url):
    regions = {}

    soup = get_soup(url)
    if soup:
        divs = soup.findAll("div", {"class": "col-md-12"})
        for div in divs[4:6]:
            links = div.findAll('a')
            for link in links:
                regions[link['href'].replace('/', '')] = dict(name=link.string.split(' (')[0], href=link['href'], stations_count=int_checker(link.string.split(' (')[1].replace(')','')))
    return regions

#функция поиска данных об АЗС на странице региона
def find_region_stations(region_key, region_soup, stations):
    for station in region_soup.findAll('div', {'class': 'item-entry'}):
        #получаем название сети АЗС
        try:
            network = station.findAll('span', {'class': 'pull-left'})[0].text.split(' ')[3]
        except (IndexError):
            network = station.findAll('span', {'class': 'pull-left'})[0].text.split(' ')[2]
        #получаем навание АЗС
        station_name = station.find('a').text
        #получаем ссылку на АЗС
        station_href = station.find('a')['href']
        #Получаем название города если оно есть
        try:
            city_name = station.findAll('span', {'class': 'pull-left'})[1].find('a').text
        except (IndexError, AttributeError):
            city_name = None
        #Получаем ссылку на город если она есть
        try:
            city_href = station.findAll('span', {'class': 'pull-left'})[1].find('a')['href']
        except (IndexError, TypeError):
            city_href = None
        #записываем все данные об АЗС в словарь stations
        stations.append(dict(region=region_key['name'], network=network, station=station_name, station_href=station_href, city=city_name, city_href=city_href))


#функция которая проходит по всем страницам региона и на каждой странице ищет список АЗС этого региона
def get_region_gas_stations(region, stations, page_number = 1):
    #формируем адрес страницы города
    retion_path = create_region_path(settings.SRC[0], region, page_number)
    region_soup = get_soup(retion_path)
    #если страница существует забираем с нее данные о АЗС
    if region_soup:
        find_region_stations(region, region_soup, stations)
        ##рекурсивно запускаем вторую страницу
        get_region_gas_stations(region, stations, page_number + 1) 

#функция которая проходит по списку регионов и записывает данные обо всех АЗС всех регионов в словарь
def get_gas_stations(regions):
    stations_count = 0
    regions_count = 0
    stations = []
    for key, value in regions.items():
        print('{:.<40}'.format(key), end='')
        get_region_gas_stations(value, stations)
        regions_count += 1
        print('OK')
    stations_count += len(stations)
    print('Загружено {} АЗС из {} регионов'.format(stations_count, regions_count))
    return stations

#функция которая получает данные об АЗС
def get_station_data(station):
    station_path = settings.SRC[0] + station['station_href']
    station_soup = get_soup(station_path)
    if station_soup:
        description = station_soup.find('div', {'class': 's-property-content'}).find('p').text
        lat = description.split('широта ')[1].replace('\n', '').split('°')[0]
        lon = description.split('долгота ')[1].replace('\n', '').split('°')[0]
        address = description.split('адресу ')[1].split(', вы')[0]
        fuel_headers = station_soup.findAll('span', {'class': 'col-xs-6 col-sm-4 col-md-4 add-d-title'})
        fuel_details = station_soup.findAll('span', {'class': 'col-xs-6 col-sm-8 col-md-8 add-d-entry'})
        station_fuel = {}
        for index in range(len(fuel_headers)):
            key = fuel_headers[index].text
            try:
                date_last_updated = date_translate(fuel_details[index].text.strip().split('обновлено ')[1].split(' г.)')[0])
                date_last_updated = int(time.mktime(datetime.datetime.strptime(date_last_updated, "%d %m %Y").timetuple()))
            except (IndexError):
                date_last_updated = None
            station_fuel[key] = dict(cost=fuel_details[index].text.strip().split(' ')[0], updated=date_last_updated)
        return dict(
            fuel = station_fuel, 
            href=station['station_href'], 
            name=station['station'], 
            region=station['region'], 
            city=station['city'], 
            network=station['network'],
            address=address,            
            lat=lat, lon=lon
        )
    return False

#Функция которая проходит по списку станций и записывает данные о станции в структуру
def get_gas_stations_data(stations):
    stations_data = {}
    time_start = int(datetime.datetime.now().timestamp())
    stations_counter = 0
    for station in stations:
        try:
            if station['network'] not in stations_data:
                stations_data[station['network']] = []
            stations_data[station['network']].append(get_station_data(station))
            stations_counter += 1
        except (KeyboardInterrupt):
            print('Остановлено вручную')
            break
    time_finish = int(datetime.datetime.now().timestamp())
    print('Загружено {} АЗС за {}'.format(stations_counter, calc_duration(time_start, time_finish)))
    return stations_data

#есил выполнить файл то в папку data/ будут сложены данные о регионах и АЗС
if __name__ == '__main__':
    regions = find_regions(settings.SRC[0])
    json_to_file(regions,'data/regions.json')
    stations = get_gas_stations(regions)
    json_to_file(stations, 'data/stations.json')
    stations_data = get_gas_stations_data(stations)
    json_to_file(stations_data, 'data/stations_data.json')