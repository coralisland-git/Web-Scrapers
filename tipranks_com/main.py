import csv
import re
import pdb
import requests
from lxml import etree
import json


base_url = 'https://www.tipranks.com'

def validate(item):    
    if item == None:
        item = ''
    if type(item) == int or type(item) == float or type(item) == bool:
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


def get_tree_items(parent, key, value, output):
    if parent != '':
        key = parent + '_' + key
    if type(value) != list:
        if type(value) == dict:
            for c_key, c_value in value.items():
                get_tree_items(key, c_key, c_value, output)
        else:
            output[key] = validate(value)


def main():
    output_list = []
    o_header = []
    session = requests.Session()
    url = 'https://finviz.com/quote.ashx?t=CHRS'
    for idx in range(0, 100):
        response = session.get(url)
        data = etree.HTML(response.text)
        table = data.xpath('.//tr[@class="table-dark-row"]')        

    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        login_url = "https://www.tipranks.com/api/users/signin"
        login_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cookie': 'tr-experiments-version=1.13; tipranks-experiments=%7b%22Experiments%22%3a%5b%7b%22Name%22%3a%22first-few-analyst-ratings%22%2c%22Variant%22%3a%22default%22%2c%22SendAnalytics%22%3afalse%7d%2c%7b%22Name%22%3a%22go-pro-variant%22%2c%22Variant%22%3a%22v1%22%2c%22SendAnalytics%22%3afalse%7d%2c%7b%22Name%22%3a%22checkout-page-variant%22%2c%22Variant%22%3a%22tipranks%22%2c%22SendAnalytics%22%3atrue%7d%5d%7d; filters={%22sector%22:%22general%22%2C%22period%22:%22yearly%22%2C%22benchmark%22:%22none%22}; abtests=0,1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        payload = {
            "email": '[email]',
            "password": '[password]'
        }
        login_response = session.post(login_url, headers=login_headers, data=json.dumps(payload))
        headers = {
            'Accept': '*/*',
            'Cookie': 'tr-experiments-version=1.13; tipranks-experiments=%7b%22Experiments%22%3a%5b%7b%22Name%22%3a%22first-few-analyst-ratings%22%2c%22Variant%22%3a%22default%22%2c%22SendAnalytics%22%3afalse%7d%2c%7b%22Name%22%3a%22go-pro-variant%22%2c%22Variant%22%3a%22v1%22%2c%22SendAnalytics%22%3afalse%7d%2c%7b%22Name%22%3a%22checkout-page-variant%22%2c%22Variant%22%3a%22tipranks%22%2c%22SendAnalytics%22%3atrue%7d%5d%7d; filters={%22sector%22:%22general%22%2C%22period%22:%22yearly%22%2C%22benchmark%22:%22none%22}; abtests=0,1; token=46bf7e495bae67e8e770f925bc7e8682bbe7372a; user=p.doritis%40gmail.com%2cpanos%2c; loginType=login; hadHoldings=true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        stock_url_1 = 'https://www.tipranks.com/api/liveFeeds/GetLatestAnalystRatings/?isBlockMain=false&top=400&countries=US&includeRatingsPreview=buy,sell&break=1578766023444'
        stock_response_1 = session.get(stock_url_1, headers=headers)
        stock_list_1 = json.loads(stock_response_1.text)['analysts']
        stock_url_2 = 'https://www.tipranks.com/api/liveFeeds/GetLatestAnalystRatings/?isBlockMain=false&top=100&countries=Canada&includeRatingsPreview=undefined&break=1578766023445'
        stock_response_2 = session.get(stock_url_2, headers=headers)
        stock_list_2 = json.loads(stock_response_2.text)['analysts']
        stock_list = stock_list_1 + stock_list_2
        for idx, stock in enumerate(stock_list):
            stock = stock_list[idx]
            output = {}
            for s_key, s_item in stock.items():
                get_tree_items('', s_key, s_item, output)

            analyst_url = 'https://www.tipranks.com/api/stocks/getData/?name='+validate(stock.get('stockTicker'))+'&benchmark=1&period=3'
            analyst_response = session.get(analyst_url, headers=headers)
            analyst = json.loads(analyst_response.text)
            for a_key, a_item in analyst.items():
                get_tree_items('', a_key, a_item, output)

            real_time_url = 'https://market.tipranks.com/api/details/GetRealTimeQuotes/?tickers='+validate(stock.get('stockTicker'))
            real_time_response = session.get(real_time_url, headers=headers)
            real_time = json.loads(real_time_response.text)[0]
            for r_key, r_item in real_time.items():
                get_tree_items('', r_key, r_item, output)

            # o_body = []
            if idx == 0:     
                for k, v in output.items():
                    o_header.append(k)
                    # o_body.append(v)

                writer = csv.DictWriter(output_file, fieldnames = o_header)
                writer.writeheader()
            new_output = {}
            for hr in o_header:
                new_output[hr] = output.get(hr)

            writer.writerow(new_output)

if __name__ == '__main__':
    main()
