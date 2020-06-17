from datetime import datetime
import os
import csv
import requests
from lxml import etree
import json
import logging
import threading
import time
import random
import multiprocessing.pool as mpool


THREAD_COUNT = 50
csv_writer_lock = threading.Lock()
session = requests.Session()


def validate(item):    
    if item == None:
        item = ''
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').decode("utf-8").strip()


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
        if item != '':
            rets.append(item)
    return rets


def parse_domain(domain, idx):
    output_file = open('output_1.csv', mode='w', newline='')
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    page = 1
    while True:
        url = "https://onshopify.com{}/{}".format(domain, page)
        source = session.get(url).text
        response = etree.HTML(source)
        store_list = eliminate_space(response.xpath('//button[@class="btn btn-default pull-left"]//text()'))
        print('{} index: '.format(domain), idx, page)
        if len(store_list) == 0:
            break
        for store in store_list:
            with csv_writer_lock:
                writer.writerow([domain.split('/')[-1], store])
        page += 1


def main():
    idx = 1
    while True:
        url = 'https://onshopify.com/domains/{}'.format(idx)
        source = session.get(url).text
        response = etree.HTML(source)
        domain_list = eliminate_space(response.xpath('//div[@class="table-responsive"]//a/@href'))
        if len(domain_list) == 0:
            break
        pool = mpool.ThreadPool(THREAD_COUNT)
        for domain in domain_list:            
            pool.apply_async(parse_domain, args=(domain, idx,))
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
