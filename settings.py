import local_settings

# сайт SRC[0] содержит общие данные об АЗС РФ, защиты от парсинга нет
# сайт SRC[1] содержит расширенные данные об АЗС РФ, блокирует IP в случае запроса данных без хедеров

SRC = ['https://mimobaka.ru', 'https://www.benzin-price.ru']
