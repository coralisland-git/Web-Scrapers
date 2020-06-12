# -*- coding: utf8 -*-
from datetime import datetime
import os
import csv
import requests
from lxml import etree
import json
import logging
import pdb
import time
import random
import math


def validate(item):
    if item == None:
        item = ''
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.strip().replace('\n', '').replace('\t', '')


def eliminate_space(items):
    rets = []
    for item in items:
        item = validate(item)
        if item != '':
            rets.append(item)
    return rets


def get_value(items):
    items = eliminate_space(items)
    if len(items) > 1:
        return items[0]
    else:
        return ''


def main():
    range_hours = input('Hour range:')
    if range_hours == '':
        range_hours = 24
    else:
        try:
            range_hours = int(range_hours)
        except Exception as e:
            print('Invalid Format')
            exit(0)
    now = datetime.now().strftime('%H:%M, %d/%m/%Y')
    now_stmp = datetime.strptime(now, '%H:%M, %d/%m/%Y')
    session = requests.Session()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'cookie': 'newrelicInited=0; newrelic_cdn_name=CF; PHPSESSID=pm3a1noil21fcvdvhm45u01ujd; mobile_default=desktop; dfp_segment_test_v3=72; dfp_segment_test=89; dfp_segment_test_v4=86; dfp_segment_test_oa=42; lister_lifecycle=1589656262; fingerprint=MTI1NzY4MzI5MTs0OzA7MDswOzA7MDswOzA7MDswOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzE7MTsxOzA7MDsxOzE7MTsxOzE7MTsxOzE7MTsxOzA7MTsxOzA7MTsxOzE7MDswOzA7MDswOzA7MTswOzE7MTswOzA7MDsxOzA7MDsxOzE7MDsxOzE7MTsxOzA7MTswOzM3MzMzOTI0NzI7MjsyOzI7MjsyOzI7MzsxMjM3Njc3NTc5OzE2NTk1ODk2NDk7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzA7MDswOzQxMDAyMTk5OzUzODA5ODc3ODsyMDU1MTc4ODI0OzMzMDgzODg0MTsxMDA1MzAxMjAzOzEzNjY7NzY4OzI0OzI0OzEyMDs2MDsxMjA7NjA7MTIwOzYwOzEyMDs2MDsxMjA7NjA7MTIwOzYwOzEyMDs2MDsxMjA7NjA7MTIwOzYwOzEyMDs2MDswOzA7MA==; dfp_user_id=cac0276d-c1f3-ba23-fcda-4a0f24f9e56e-ver2; random_segment_js=81; used_adblock=adblock_disabled; ldTd=true; cX_P=kaa0av91h0bwmzkq; cxsegment=; _ga=GA1.2.331525184.1589656274; _gid=GA1.2.566210852.1589656274; _gat_clientNinja=1; optimizelyEndUserId=oeu1589656274598r0.9911975148339911; lqstatus=1589657475; laquesis=disco-773@b#olxeu-29990@c#olxeu-30294@a#olxeu-30387@c#search-273@a; laquesisff=olxeu-29763; cX_S=kaa0avo0mzozqblo; olxRebrandedWelcomeClosed=1; evid_0046=c50abe13-14f6-4625-a0c5-0a3341c75a90; adptset_0046=1; evid_set_0046=2; cstp=1; mktz_sess=sess.2.1636084118.1589656277514; mktz_client=%7B%22is_returning%22%3A0%2C%22uid%22%3A%221159830144475614297%22%2C%22session%22%3A%22sess.2.1636084118.1589656277514%22%2C%22views%22%3A1%2C%22referer_url%22%3A%22%22%2C%22referer_domain%22%3A%22%22%2C%22referer_type%22%3A%22direct%22%2C%22visits%22%3A1%2C%22landing%22%3A%22https%3A//www.olx.ro/oferte/%22%2C%22enter_at%22%3A%222020-05-16%7C21%3A11%3A17%22%2C%22first_visit%22%3A%222020-05-16%7C21%3A11%3A17%22%2C%22last_visit%22%3A%222020-05-16%7C21%3A11%3A17%22%2C%22last_variation%22%3A%22%22%2C%22utm_source%22%3Afalse%2C%22utm_term%22%3Afalse%2C%22utm_campaign%22%3Afalse%2C%22utm_content%22%3Afalse%2C%22utm_medium%22%3Afalse%2C%22consent%22%3A%22%22%7D; user_adblock_status=true; cX_G=cx%3A3az04x4bwh7qx29xxk0fs8c7ln%3A1tbvc2t2ocjpf; __sreff=1589656279839.1589656279839.1; __reff=[[www.olx.ro/oferte/]](direct)&1589656279839.1589656279839.1; cookieBarSeen=true; consentBarSeen=true; didomi_token=eyJ1c2VyX2lkIjoiMTcyMWVlNWItZGI3OS02MzZjLWExMGUtMzdhOTM0YWFhOWYxIiwiY3JlYXRlZCI6IjIwMjAtMDUtMTZUMTk6MTE6MTQuMDYzWiIsInVwZGF0ZWQiOiIyMDIwLTA1LTE2VDE5OjExOjIyLjIyNVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIl0sImRpc2FibGVkIjpbXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llcyIsImFkdmVydGlzaW5nX3BlcnNvbmFsaXphdGlvbiIsImFkX2RlbGl2ZXJ5IiwiY29udGVudF9wZXJzb25hbGl6YXRpb24iLCJhbmFseXRpY3MiXSwiZGlzYWJsZWQiOltdfX0=; euconsent=BOzgkw0OzgkyGAHABBRODG-AAAAvRrv7__7-_9_-_f__9uj3Or_v_f__32ccL59v_h_7v-_7fi_-1jV4u_1vft9yfk1-5ctDztp507iakivXmqdeb1v_nz3_9phP78k89r7337Ew-OkAAAAAAAAAAAAAAAAA; cmpvendors=4; cmpreset=true; onap=1721ee5bda0x6a1b1de2-1-1721ee5bda0x6a1b1de2-8-1589658084',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    flag = True
    page = 1
    filename = '{}.csv'.format(datetime.now().strftime('%Y%m%d%H%M%S'))
    with open(filename, mode='w', encoding="utf-8-sig", newline='') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow([
            'Price', 'Title', 'Url', 'Location', 'Description', 'Id', 'Time of posting', 'Image', 'Category', 'Model', 'Year'
        ])        
        while flag:
            page_url = 'https://www.olx.com.lb/en/ads/?page={}'.format(page)
            response = session.get(page_url, headers=headers).text
            data = etree.HTML(response)
            ads_list = data.xpath('.//div[contains(@class, "ads--list")]//a[@class="ads__item__ad--title"]/@href')
            for ads_link in ads_list:        
                ads_link = ads_link.replace('/ad/', '/en/ad/').replace('/ads/', '/en/ads/')
                output = []
                ads = etree.HTML(session.get(ads_link, headers=headers).text)
                sub_ads_list = ads.xpath('.//div[contains(@class, "ads--list")]//a[@class="ads__item__ad--title"]/@href')
                if len(sub_ads_list) != 0:
                    continue
                id = validate(ads.xpath('.//span[@class="rel inlblk"]//text()'))
                category = ''.join(eliminate_space(ads.xpath('.//table[@id="breadcrumbTop"]//ul//text()')))
                time = eliminate_space(validate(ads.xpath('.//span[@class="pdingleft10 brlefte5"]//text()')).replace(id, '').strip().split(','))
                dt = time[0].split(' ')[-1] + ', ' + time[1]
                dt_stmp = datetime.strptime(dt, '%H:%M, %d %b %Y')
                delta = math.ceil((now_stmp - dt_stmp).total_seconds()/3600)
                test_stmp = datetime.strptime('15:12, 13 May 2020', '%H:%M, %d %b %Y')
                model = ''
                year = ''
                details = ads.xpath('.//table[@class="item"]')
                for detail in details:
                    th = validate(detail.xpath('.//th//text()')).lower()
                    value = validate(detail.xpath('.//td//text()')).lower()
                    if 'model' in th:
                        model = value
                    if 'year' in th:
                        year = value
                if delta < range_hours:
                    output = [
                        validate(get_value(ads.xpath('.//div[@class="pricelabel tcenter"]//text()'))), #price
                        validate(ads.xpath('.//h1[@class="brkword lheight28"]//text()')), #title
                        ads_link,
                        validate(ads.xpath('.//span[@class="show-map-link link gray cpointer"]//text()')), #location
                        validate(ads.xpath('.//div[@id="textContent"]//text()')), #description
                        id, #id,
                        dt, #time of posting
                        validate(get_value(ads.xpath('.//img[contains(@class, "vtop bigImage")]/@src'))), #image
                        category, #category
                        model, #model for car
                        year #year for car
                    ]
                    print(ads_link)
                    writer.writerow(output)
                else:
                    flag = False
                    break
            page += 1


if __name__ == '__main__':
    main()
