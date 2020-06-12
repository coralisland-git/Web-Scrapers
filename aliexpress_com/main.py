import csv
import re
import pdb
import requests
from lxml import etree
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


def validate(item):    
    if item == None:
        item = ''
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.replace(u'\u2013', '-').encode('ascii', 'ignore').encode("utf8").strip()

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

def main():
    output_list = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    with open('aliexpressProducts.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["Product Url", "Order Count"])
        urls = [
            'https://www.aliexpress.com/af/category/1511.html?trafficChannel=af&catName=watches&CatId=1511&ltype=affiliate&SortType=total_tranpro_desc&g=n&page={}&groupsort=1&isrefine=y', # watch 
            'https://www.aliexpress.com/af/category/30.html?trafficChannel=af&catName=security-protection&CatId=30&ltype=affiliate&SortType=total_tranpro_desc&groupsort=1&isrefine=y&page={}', # security
            'https://www.aliexpress.com/af/category/7.html?trafficChannel=af&catName=computer-office&CatId=7&ltype=affiliate&SortType=total_tranpro_desc&groupsort=1&isrefine=y&page={}', # computer && office
            'https://www.aliexpress.com/af/category/15.html?trafficChannel=af&catName=home-garden&CatId=15&ltype=affiliate&SortType=total_tranpro_desc&g=n&page={}&groupsort=1&isrefine=y', # home
        ]
        for url_origin in urls:
            edge = True
            page = 1
            while edge:
                url = url_origin.format(page)
                print(page, url)
                driver.get(url)
                response = driver.page_source
                data = validate(response.split('window.runParams =')[2].split('window.runParams.csrfToken')[0])[:-1]
                products = json.loads(data)['items']
                for product in products:
                    p_url = 'https:'+validate(product.get('productDetailUrl'))
                    driver.get(p_url)
                    p_response = driver.page_source
                    p_data = '{'+validate(p_response.split('data: {')[1].split('csrfToken:')[0])[:-1]
                    p_order = json.loads(p_data).get('titleModule').get('formatTradeCount')
                    try:
                        if int(p_order) < 5000:
                            edge = False
                            break
                    except Exception as e:
                        print e
                    output = [
                        p_url, p_order, url
                    ]                
                    writer.writerow(output)
                    time.sleep(3)
                page += 1

if __name__ == '__main__':
    main()
