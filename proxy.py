from datetime import datetime, timezone


class ProxiesQueue():
    def __init__(self):
        with open('proxy_http_ip.txt', 'r') as fin:
            self.proxies = dict([(x.split(':')[0], int(datetime.utcnow().timestamp())) for x in fin.readlines()])
    
    def get_active_proxy(self):
        for proxy, active_time in self.proxies.items():
            if active_time <= int(datetime.utcnow().timestamp()):
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
        self.proxies[proxy] += ban_time * 60

n = ProxiesQueue()
for i in range(10):
    p = n.get_active_proxy()
    n.ban_proxy(p)
    print(f"proxy{p} baned")

#возвращает случайную проксю из списка
# def get_proxy(type):
#     with open('proxy_http_ip.txt', 'r') as fin:
#         proxy_list = [x.split(':')[0] for x in fin.readlines()]
#     if type == 'http':
#         return f"{choice(proxy_list)}:8085"
#     if type == 'socks':
#         return f"{choice(proxy_list)}:1085"
#     if type == 'ssl':
#         return f"{choice(proxy_list)}:8085"
#     return False