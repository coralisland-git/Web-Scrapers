import csv
import sys
import requests
from bs4 import BeautifulSoup
# import deathbycaptcha
from config import DBC_PASSWORD, DBC_USERNAME, CAPTCHA_KEY
import config
from datetime import date
import datetime
from send_mail import send_email
import logging
import io
from lxml import etree
import pdb
import time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=bokf0lngt4cn1myyutolc3l1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}

""" Client for http://webapps.hcso.tampa.fl.us/ArrestInquiry """
class HillsClient(object):
    def __init__(self, start_date, days = 1):
        """
        :start_date :: datetime.date, The first date for which arrest records
          are desired.
        :days :: int, The total number of days for which arrest records are
          desired. Use '1' if records for start_date only are desired.
        """
        self.session = requests.session()
        self.session.headers.update(headers)

        # self.main_url = "http://webapps.hcso.tampa.fl.us/ArrestInquiry/"
        # self.base_url = "http://webapps.hcso.tampa.fl.us"

        self.main_url = "https://webapps.hcso.tampa.fl.us/ArrestInquiry/"
        self.base_url = "https://webapps.hcso.tampa.fl.us"

        self.data_sitekey = '6LdMkrsUAAAAAHzYKwFUq90nkLEk9EEW04RVQbtV'

        self.captcha_guid = None

        self.current_page = 1
        self.total_results = 0

        # Validate `days`
        if days < 1:
            raise ValueError("'days' must not be less than 1.")

        # Create a set of dates.
        self.dates = [start_date + datetime.timedelta(days=x) for x in range(0, days)]
    
    def get_date(self,days=0):
        today = date.today()

        dt_target = today  - datetime.timedelta(days=days)

        today_str = dt_target.strftime('%m/%d/%Y')

        return today_str

    def validate(self,item):
        if item == None:
            item = ''
        if type(item) == int or type(item) == float:
            item = str(item)
        if type(item) == list:
            item = ' '.join(item)
        return item.replace(u'\u2013', '-').strip().replace('\t', '').replace('\n', ' ')

    def eliminate_space(self,items):
        rets = []
        for item in items:
            item = self.validate(item)
            if item != '':
                rets.append(item)
        return rets

    def run(self):
        """
        Main entry point to functionality.
        Returns an array of arrest records.
        """
        all_recs = []
        for date in self.dates:
            captcha_id = requests.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(CAPTCHA_KEY, self.data_sitekey, self.main_url)).text.split('|')[1]
            captcha_text = requests.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(CAPTCHA_KEY, captcha_id)).text
            while 'CAPCHA_NOT_READY' in captcha_text:
                time.sleep(5)
                captcha_text = requests.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(CAPTCHA_KEY, captcha_id)).text                
            captcha_text = str(captcha_text.split('|')[1])
            formatted_date = date.strftime('%m/%d/%Y')
            cur_page = 1
            while True:
                payload = {
                    "SearchBookingNumber": '',
                    "SearchName": '',
                    "SearchBookingDate": formatted_date,
                    "SearchReleaseDate": '',
                    "SearchRace": '',
                    "SearchSex": '',                
                    "SearchCurrentInmatesOnly": "false",
                    "SearchIncludeDetails": "false",
                    "SearchSortType": "BOOKNO",
                    'g-recaptcha-response': captcha_text,
                    'SearchResults.PageSize': 200,
                    'ResultsPerPage': 200,
                    'SearchResults.CurrentPage': cur_page
                }
                response = etree.HTML(self.session.post(self.main_url, payload, headers=headers).text)
                rows = response.xpath('//table//tbody//tr')
                if len(rows) == 0:
                    break
                for row in rows:
                    tds = row.xpath('.//td')
                    output = []
                    charges = []
                    name = self.validate(tds[1].xpath('.//text()')).split(',')
                    first_name = self.validate(name[-1].title().split(' ')[0])
                    last_name = self.validate(name[0].title())
                    detail_link = self.base_url + self.validate(tds[0].xpath('.//a/@href'))
                    d_response = etree.HTML(self.session.get(detail_link).text)
                    data = self.eliminate_space(d_response.xpath('.//div[contains(@class, "default-hcso-bg")]//text()'))
                    for d_idx, dat in enumerate(data):
                        try:
                            n_dat = ''
                            if d_idx+1 < len(data) and ':' not in data[d_idx+1]:
                                n_dat = data[d_idx+1]
                            if 'Street Address:' in dat:
                                street = n_dat
                            if 'City:' in dat:
                                city = n_dat
                            if 'State:' in dat:
                                state = n_dat
                            if 'Zip:' in dat:
                                zip_code = n_dat
                            if 'Charge Description:' in dat:
                                charges.append(n_dat)
                        except Exception as e:                            
                            pass
                    output = [
                        first_name, last_name, street, city, state, zip_code
                    ]
                    output += charges[:3] if len(charges) > 3 else charges
                    all_recs.append(output)
                cur_page += 1

        return all_recs

def write_csv(file_like, content):
    writer = csv.writer(file_like, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['First Name','Last Name', 'Street','City','State','Zip','Charge1','Charge2','Charge3'])
    for ct in content:
        writer.writerow(ct)

def main():
    # Create the client
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    hc = HillsClient(yesterday, days = 2)

    # File names
    fname = str(hc.get_date()).replace('/','-')
    fname_csv = fname + '.csv'
    fname_log = fname + '.log'

    # # Logging
    level = logging.DEBUG
    root = logging.getLogger()
    root.setLevel(level)

    # Run the scraper.
    all_recs = hc.run()

    # Write the arrest records to file.
    with open(fname_csv, "w") as f:
        write_csv(f, all_recs)

    # Send the email with results attached.
    send_email(config.EMAIL_TO, subject="Hillsborough County Arrests",attachment=fname_csv)

if __name__ == '__main__':
    try:
        main()
    except:
        main()
