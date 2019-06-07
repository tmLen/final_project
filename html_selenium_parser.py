import re

import settings
from utils import get_soup_selenium

def get_regions_href(url):
    region_hrefs = []
    soup = get_soup_selenium(url)
    links = soup.findAll('a', {"href": re.compile(r'zapravka\.php\?region*')})
    for link in links:
        print(link['href'], link.string)
    return region_hrefs

if __name__ == '__main__':
    print(get_regions_href(settings.SRC[1]))