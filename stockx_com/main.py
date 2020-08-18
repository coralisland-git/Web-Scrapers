import os
import requests
from lxml import etree
import re
import json
import time
import pdb
import logging
import datetime

class Main:
    name = 'stockx'
    base_url = 'https://stockx.com'
    thread_count = 3
    init_urls = [
        'https://stockx.com'
    ]
    session = requests.Session()

    def __init__(self):
        # for url in self.init_urls:
        #     self.start_requests(url)
        url = input('URL of product:')
        if url == '' or 'http' not in url:
            print('Invalid URL')
            exit(0)
        self.start_requests(url)
    
    def start_requests(self, url):
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'cookie': '__cfduid=d36da17b50af32b269621116e432755dd1597696714; stockx_homepage=sneakers; language_code=en; stockx_market_country=US; dd_rum_test=test; _dd_r=0; _ga=GA1.2.395896576.1597696722; _gid=GA1.2.996387677.1597696722',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
            }
            response = self.session.get(url, headers=headers).text
            data = response.split('window.preLoaded = ')[1].split('};')[0] + '}'
            product =  json.loads(data)['product']
            now = datetime.date.today()
            sales_url = f'https://stockx.com/api/products/{product["id"]}/chart?start_date=all&end_date={str(now)}&intervals=100&format=highstock&currency=USD&country=US'
            sales_headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'cookie': '__cfduid=d36da17b50af32b269621116e432755dd1597696714; stockx_homepage=sneakers; language_code=en; stockx_market_country=US; dd_rum_test=test; _dd_r=0; _ga=GA1.2.395896576.1597696722; _gid=GA1.2.996387677.1597696722',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }
            sales_response = self.session.get(sales_url, headers=sales_headers).text
            sales_data = json.loads(sales_response)['series'][0]['data']
            sales = []
            for data in sales_data:
                date = self.validate(datetime.datetime.fromtimestamp(data[0]/1000).strftime('%Y-%m-%d'))
                sales.append({
                    'date': date,
                    'amount': data[1]
                })                
            output = {
                'Id': product['id'],
                'Name': product['name'],
                'Brand': product['brand'],
                'Category': product['productCategory'],
                'Gender': product['gender'],
                '# of Sales': product['market']['deadstockSold'],
                'Price premium': product['market']['pricePremium'] * 100,
                'Release Date': product['releaseDate'],
                'Retail Price': product['retailPrice'],
                'ColorWay': product['colorway'],
                'Style': product['styleId'],
                'Last Sale': product['market']['lastSale'],
                'Description': product['description'],
                'Sales': sales
            }
            self.write(output)
            print('Scraped successfully!')
        except Exception as e:
            print(f'Failed : {url} : {e}')

    def write(self, output):
        with open(f'{output["Name"]}.json', 'w') as outputfile:
            outputfile.write(json.dumps(output, indent=4))
    
    def validate(self, item):
        if item == None:
            item = ''
        if type(item) == int or type(item) == float:
            item = str(item)
        if type(item) == list:
            item = ' '.join(item)
        return item.strip()
    
    def config_log(self):
        filename = 'history.log'
        logging.basicConfig(filename=filename, level=logging.INFO)
        logging.info("Starts...")


if __name__ == '__main__':
    Main()
