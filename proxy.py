from utils import get_current_utc_timestamp

class ProxiesQueue():
    def __init__(self):
        with open('proxy_http_ip.txt', 'r') as fin:
            self.proxies = dict([(x.split(':')[0], get_current_utc_timestamp()) for x in fin.readlines()])
    
    def get_active_proxy(self):
        for proxy, active_time in self.proxies.items():
            if active_time <= get_current_utc_timestamp():
                return proxy
        raise ValueError('There is no any free proxy in proxy list')
    
    def get_proxy_port(self, type='http'):
        if type == 'http':
            return 8085
        elif type == 'ssl':
            return 1085
        elif type == 'socks':
            return 1085
        raise ValueError(f"There is no pory-type \"{type}\"")
    
    #метод который принимает на вход прокси и время на которое её нужно забанить в минутах и банит прокси
    def ban_proxy(self, proxy, ban_time=5):
        print(f"Ban proxy {proxy} for {ban_time} min")
        self.proxies[proxy] += ban_time * 60


    #прокси для requests
    # with open('proxy_http_ip.txt', 'r') as fin:
    #     proxy_list = [x.replace('\n', '') for x in fin.readlines()]
    # url = 'https://2ip.ru'
    # proxies = {'http': choice(proxy_list)}
    # reque = requests.get(url, proxies=proxies)

#прокси для selenium
#     webdriver.DesiredCapabilities.FIREFOX['proxy']={
#     "httpProxy":'ip:port',
#     "ftpProxy":'ip:port',
#     "sslProxy":'ip:port',
#     "proxyType":"MANUAL"
#             }
# driver = webdriver.Firefox()

if __name__ == '__main__':
    p = ProxiesQueue()
    for i in range(len(p.proxies) + 1):
        try:
            p.ban_proxy(p.get_active_proxy())
        except:
            print('No available proxies, try later')