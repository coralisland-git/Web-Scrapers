import time
import json
import re
import random

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
#proxy.http_proxy = 'ip_addr:port'
#proxy.socks_proxy = 'ip_addr:port'
proxy.ssl_proxy = ''
print(proxy.ssl_proxy)

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

agents = ['Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36']

options = Options()
options.add_argument('user-agent={}'.format(random.choice(agents)))
#options.add_argument('--start-maximized')
#options.add_argument('--headless')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome('chromedriver.exe', options=options,
                          desired_capabilities=capabilities)

url = 'https://www.aliexpress.com/all-wholesale-products.html'
#driver.get(url)

soup = bs(driver.page_source, 'lxml')
#categories = ['https://' + c['href'][2:] for c in soup.select('.anchor-agricuture a')]
categories = ['https://www.aliexpress.com/category/100003109/women-clothing.html', 
            'https://www.aliexpress.com/category/100003070/men-clothing.html', 
            'https://www.aliexpress.com/category/509/cellphones-telecommunications.html', 
            'https://www.aliexpress.com/category/7/computer-office.html', 
            'https://www.aliexpress.com/category/44/consumer-electronics.html', 
            'https://www.aliexpress.com/category/1509/jewelry-accessories.html', 
            'https://www.aliexpress.com/category/15/home-garden.html', 
            'https://www.aliexpress.com/category/1524/luggage-bags.html', 
            'https://www.aliexpress.com/category/322/shoes.html', 
            'https://www.aliexpress.com/category/1501/mother-kids.html', 
            'https://www.aliexpress.com/category/18/sports-entertainment.html', 
            'https://www.aliexpress.com/category/66/beauty-health.html', 
            'https://www.aliexpress.com/category/1511/watches.html', 
            'https://www.aliexpress.com/category/26/toys-hobbies.html', 
            'https://www.aliexpress.com/category/100003235/weddings-events.html', 
            'https://www.aliexpress.com/category/200000875/novelty-special-use.html', 
            'https://www.aliexpress.com/category/34/automobiles-motorcycles.html', 
            'https://www.aliexpress.com/category/39/lights-lighting.html', 
            'https://www.aliexpress.com/category/1503/furniture.html', 
            'https://www.aliexpress.com/category/502/electronic-components-supplies.html', 
            'https://www.aliexpress.com/category/21/education-office-supplies.html', 
            'https://www.aliexpress.com/category/6/home-appliances.html', 
            'https://www.aliexpress.com/category/13/home-improvement.html', 
            'https://www.aliexpress.com/category/2/food.html', 
            'https://www.aliexpress.com/category/30/security-protection.html', 
            'https://www.aliexpress.com/category/1420/tools.html', 
            'https://www.aliexpress.com/category/200002489/hair-extensions-wigs.html', 
            'https://www.aliexpress.com/category/205776616/apparel-accessories.html', 
            'https://www.aliexpress.com/category/205779615/underwear-sleepwears.html']

links = set()
for idx, category in enumerate(categories):
    print(f'{idx+1}/{len(categories)}: {category}')
    page = 1
    end = False
    time.sleep(2)
    while not end:
        url = category + f'?SortType=total_tranpro_desc&g=y&page={page}'
        driver.get(url)
        time.sleep(1)
        for _ in range(10):
            driver.execute_script('window.scrollBy(0,1000);')
            time.sleep(0.02)
        
        soup = bs(driver.page_source, 'lxml')
        cards = soup.select('div.product-card')
        if len(cards) == 0:
            break
        for card in cards:
            try:
                count = int(card.select('.sale-value-link')[0].text.split()[0])
            except IndexError:
                continue
            if count < 5000:
                end = True
                break
            link = card.a['href']
            links.add(link)
        page += 1
        print('Link count:', len(links))
    print('Links collected far:', len(links))

with open('links.txt', 'w') as f:
    f.write('\n'.join(sorted(list(links))))
    
print(f'Saved {len(links)} links.')
