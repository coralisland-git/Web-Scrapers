import csv
import re
import pdb
import requests
from lxml import etree
import sys
import json
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

def main(username, password):    
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    url = "https://crm.konnektive.com/"
    driver.get(url)
    driver.find_element_by_name('userName').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_id('loginBtn').click()
    print('logged in')

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Required usename and password')
        exit(0)  
    main(sys.argv[2], sys.argv[4])
