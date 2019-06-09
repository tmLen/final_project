from utils import get_current_utc_timestamp, timestamp_to_date
import settings

class UrlBase:
    def __init__(self):
        self.urls = {}                  #словарь для хранения url 
        self.check_frequency = 1440      #частота обновления данных в минутах
    
    #метод добавления url в базу, время следующей проверки = текущему
    def add_url(self, url):
        if url not in self.urls:
           self. urls[url] = get_current_utc_timestamp()
    
    #метод вызова url на проверку - меняет время следующей проверки на текущее
    def call_for_check(self, url):
        self. urls[url] = get_current_utc_timestamp()
    
    #метод который позволяет отложить проверку на определенное количество минут
    def postpone_check(self, url, postpone_time = 0):
        if postpone_time == 0:
            postpone_time = self.check_frequency
        self.urls[url] = get_current_utc_timestamp() + postpone_time * 60
    
    #метод выбирает url который надо проверить и возвращает его
    def get_url_for_check(self):
        for (url, check_time) in self.urls.items():
            if check_time <= get_current_utc_timestamp():
                return url
            

    #перегрузка вывода
    def __repr__(self):
        return "\n".join("url's {} check time is {}".format(url, timestamp_to_date(check_time))
            for (url, check_time) in self.urls.items()
            )


if __name__ == '__main__':
    urls = UrlBase()
    urls.add_url(settings.SRC[0])
    urls.add_url(settings.SRC[1])
    print(urls.get_url_for_check(), '\n')
    print(urls, '\n')
    urls.postpone_check(settings.SRC[0])
    print(urls)