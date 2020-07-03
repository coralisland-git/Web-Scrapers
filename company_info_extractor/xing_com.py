# -*- coding: utf8 -*-
import csv
import re
from lxml import etree
import json
import os
import pdb
import requests


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
        writer.writerow(['name', 'employment status', 'position', 'company'])
        for file_name in load_files():
            if '.htm' not in file_name:
                continue
            with open('data/{}'.format(file_name), 'r') as inputfile:
                content = inputfile.read()
                tree = etree.HTML(content)
        
            data_list = tree.xpath('.//div[contains(@class, "MembersResults-MembersResults-container")]//div[contains(@class, "search-result-card-SearchResultCard-content")]')
            for data in data_list:
                name = validate(data.xpath('.//div[contains(@class, "search-result-card-SearchResultCard-badgedTitle")]//text()'))
                values = eliminate_space(data.xpath('.//p[contains(@class, "bodyCopy-medium-text")]//text()'))
                output = [
                    name,
                    values[0].replace(',', ''),
                    values[1],
                    values[2]
                ]                
                writer.writerow(output)

if __name__ == '__main__':
    main()
