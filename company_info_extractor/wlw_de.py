# -*- coding: utf8 -*-
import csv
import re
from lxml import etree
import json
import os
import pdb
import requests


base_url = 'https://www.wlw.de'

def validate(item):    
    if item == None:
        item = ''
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.strip()

def get_value(item):
    if item == None :
        item = '<MISSING>'
    item = validate(item)
    if item == '':
        item = '<MISSING>'    
    return item

def eliminate_space(items):
    rets = []
    for item in items:
        item = validate(item)
        if item != '' and item != ',':
            rets.append(item)
    return rets

def load_files():
    arr = os.listdir('./data')
    return arr

def main():
    with open('output.csv', mode='w', encoding="utf-8-sig", newline='') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['name', 'address', 'url'])
        session = requests.Session()
        url = 'https://www.wlw.de/de/firmen/elektroinstallationen'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cookie': 'wlw_locale=de; wlw_search_term=Elektroinstallationen; wlw_client_id=rBEAHV7/WikRrQDyA2iGAg==; _ga=GA1.2.397582320.1593793072; _gid=GA1.2.637220284.1593793072; _hjid=e3cd60d9-5a2e-47fc-a65d-1ae60c1304f3; _hjIncludedInSample=1; _hjAbsoluteSessionInProgress=1; axd=4231071253802279745; AMCVS_41833DF75A550B4B0A495DA6%40AdobeOrg=1; AMCV_41833DF75A550B4B0A495DA6%40AdobeOrg=-1303530583%7CMCIDTS%7C18447%7CMCMID%7C57073394443232204350719483588446118366%7CMCAAMLH-1594397876%7C9%7CMCAAMB-1594397876%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1593800276s%7CNONE%7CvVersion%7C3.3.0; AAMC_iqdigital_0=REGION%7C9; __hstc=80469576.89aed86ba432e381fc3bcdb33372f980.1593793082552.1593793082552.1593793082552.1; hubspotutk=89aed86ba432e381fc3bcdb33372f980; __hssrc=1; __zlcmid=z0jFxeJQ8HLCgL; category_id=78871; _wlw_common_session=GEIVD46vb9rzfZvZfHEKfALRSnjnd9KxYPcP5zAN1hj4gcbX93%2F7%2BpMue2ws6W4yDxrFRb1FfUhjkgI%2Fp%2Bj2y%2BEJvTs6pYENYL%2BpttgWwQpN5IOyKM452do6EecVq7Iq2wruU2lq8BuNSiS58YQ%3D--Wj357LNMFXlYejai--qpv9c8Xat5auHgOkM3FvsQ%3D%3D; __hssc=80469576.2.1593793082553; _gat_UA-38607859-4=1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        response = session.get(url, headers=headers)
        tree = etree.HTML(response.text)
        page_count = 0
        try:
            page_count = int(tree.xpath('.//ul[@class="pagination"]//li[@class="hidden-xs"]//text()')[-1]) + 1
        except:
            pass
        for page in range(1, page_count):
            block_url = '{}?page={}'.format(url, page)
            parse_block(session, block_url, headers, writer)

def parse_block(session, url, headers, writer):
    response = session.get(url, headers=headers)
    tree = etree.HTML(response.text)
    data_list = tree.xpath('.//article[contains(@class, "panel panel--company")]')
    for data in data_list:
        name = validate(data.xpath('.//div[contains(@class, "h4 panel__title")]//text()'))
        link = base_url + validate(data.xpath('.//div[contains(@class, "h4 panel__title")]/a/@href'))
        p_response = session.get(link, headers=headers)
        p_tree = etree.HTML(p_response.text)
        address = ', '.join(eliminate_space(p_tree.xpath('.//address[contains(@class, "location-and-contact__address")]//div//text()')))
        output = [
            name, address, url
        ]
        writer.writerow(output)
        print(output)

if __name__ == '__main__':
    main()
