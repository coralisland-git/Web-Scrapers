# -*- coding: utf8 -*-
import csv
import re
from lxml import etree
import json
import os
import pdb


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
        writer.writerow(['name', 'position', 'company'])
        for file_name in load_files():
            if '.htm' not in file_name:
                continue
            with open('data/{}'.format(file_name), 'r') as inputfile:
                content = inputfile.read()
                tree = etree.HTML(content)
            data_list = tree.xpath('.//li[contains(@class, "search-result search-result__occluded-item ember-view")]')
            for data in data_list:
                name = validate(data.xpath('.//span[contains(@class, "name actor-name")]//text()'))
                pos_and_com = validate(data.xpath('.//p[contains(@class, "subline-level-1")]//text()'))
                if ' bei ' in pos_and_com:
                    pos_and_com = pos_and_com.split(' bei ')
                    output = [
                        name, pos_and_com[0], pos_and_com[1]
                    ]
                else:
                    output = [
                        name, pos_and_com, ''
                    ]                
                writer.writerow(output)

if __name__ == '__main__':
    main()
