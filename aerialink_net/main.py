#!/usr/bin/python
# coding=utf-8
import csv
import re
import pdb
import requests
from lxml import etree
import json
import sys


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


def load_code_list():
    code_list = []
    with open('codes.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            code_list.append(
                {
                    'number' : validate(row[0]),
                    'text' : validate(row[1])
                }
            )
    return code_list            


def main(username, password):
    base_url = 'https://platform.aerialink.net'
    session = requests.Session()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    login_url = 'https://platform.aerialink.net/login'
    login_form = {
        'utf8': '%E2%9C%93',
        'userName': username,
        'password': password
    }
    login_response = session.post(login_url, headers=headers, data=login_form)
    if login_response.headers.get('Status') == '403 Forbidden':
        print('Incorrect username or password')
        exit(0)
    print('Logged in successfully')
    headers['Cookie'] = login_response.headers.get('Set-Cookie')
    for code in load_code_list():
        try:
            url = "https://platform.aerialink.net/codes?utf8=%E2%9C%93&connection_guid=&search_code={}&shared_code=&code_type=&service%5Bsms%5D=1&service%5Bmms%5D=1&service%5Blbs%5D=1&service%5Bdms%5D=1&service%5Bvoice%5D=1".format(code['number'])
            response = etree.HTML(session.get(url, headers=headers).text)
            links = eliminate_space(response.xpath('.//ul[@class="code-list"]//a/@href'))
            if len(links) > 0:
                link = base_url + links[0]
                data = session.get(link, headers=headers).text
                phone_response = etree.HTML(data)
                select_list = phone_response.xpath('.//select[@id="code_new_connection_id"]//option')        
                new_id = ''
                old_id = ''
                for select in select_list:
                    value = validate(select.xpath('./@value'))
                    text = validate(select.xpath('.//text()'))
                    selected = validate(select.xpath('./@selected'))
                    if selected == 'selected':
                        old_id = value
                    if code['text'] in text:
                        new_id = value
                authenticity_token = validate(phone_response.xpath('.//input[@name="authenticity_token"]/@value'))
                submit_link = link.replace('/edit', '')
                formdata = {
                    'utf8': '%E2%9C%93',
                    '_method': 'patch',
                    'authenticity_token': authenticity_token,
                    'code[name]': '',
                    'code[emailAddress]': '',
                    'code[emailTemplateID]': 0,
                    'code[voiceForwardTypeID]': 0,
                    'code[voiceForwardDestination]': '',
                    'code[new_connection_id]': new_id,
                    'code[old_connection_id]': old_id,
                    'code[mms_enable]': 0,
                    'code[mms_enable]': 1,
                    'commit': 'Update Code'
                }
                submit_response = session.post(submit_link, headers=headers, data=formdata)                
                print(code['number'], code['text'], submit_response.headers.get('Status'))
        except Exception as e:
            pass
    print('Finished')


if __name__ == '__main__':
    print('Provide your login, Please...')
    print('-----------------------------')
    username = raw_input("username: ")
    password = raw_input("password: ")
    print('-----------------------------')
    if username == '' or password == '':
        print('Required username and password')
        exit(0)    
    main(username, password)
