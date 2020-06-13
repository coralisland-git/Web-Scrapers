import lxml.html
import requests
import re
from lxml import etree
from io import StringIO
from urllib3.exceptions import InsecureRequestWarning
import csv
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import threading, queue


headers = ('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36')
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
jobs = queue.Queue(maxsize=10)


def worker(f):
    global jobs
    while True:
        job = jobs.get()
        try:
            [school,street,town,county,postcode,website,tel,type] = scrape_entry('http://schoolswebdirectory.co.uk/%s' % job)
            f.writerow([school,street,town,county,postcode,website,tel,'',type])
        except:
            pass
        jobs.task_done()


def worker2(f):
    global jobs
    while True:
        job = jobs.get()
        try:
            [school,street,town,county,postcode,website,tel,emails,type] = job.split(',')
            try:
                emails = scrape_emails(website)
            except Exception as e:
                print(e)
            f.writerow([school,street,town,county,postcode,website,tel,emails,type[:-1]])
            print([school,street,town,county,postcode,website,tel,emails,type[:-1]])
        except Exception as e:
            print(e)
        jobs.task_done()


def scrape_emails(url, level=0):
    emails = []
    contact_pages = []
    req = urllib2.Request(url)
    u_str = url.split('/')    
    domain = '{}//{}'.format(u_str[0], u_str[2])
    req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36')
    html_page = urllib2.urlopen(req)
    soup = BeautifulSoup(html_page,features='html.parser')
    blacklist = [
        'noscript',
        'meta',
        'head',
        'script',
    ]
    texts = soup.findAll(text=True)
    content = ''
    for t in texts:
        if t.parent.name not in blacklist:
            content += '{} '.format(t)
    h_emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", content)    
    for e in h_emails:
        if e in emails:
            continue
        emails.append(e)
    for link in soup.findAll('a'):
        val = link.get('href')
        text = link.getText().lower()
        if ( (val != None and 'contact' in val.lower()) or (text != None and 'contact' in text) ) and val not in contact_pages:
            if '://' not in val:
                val = '{}{}{}'.format(domain, '' if val[0] == '/' else '/', val)                
            contact_pages.append(val)
    if level == 0:
        for page in contact_pages:
            for e in scrape_emails(page, 1):
                if e in emails:
                    continue
                emails.append(e)
    return emails


def scrape_entry(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page,features='lxml')
    school = str(soup.select('tr:nth-child(7) .infotext3 font')[0]).replace('<font size="3">', '').replace('</font>','')
    street = str(soup.select('tr:nth-child(8) .infotext3 font')[0]).replace('<font size="2">', '').replace('</font>','')
    town = str(soup.select('tr:nth-child(9) .infotext3 font')[0]).replace('<font size="2">', '').replace('</font>','')
    county = str(soup.select('tr:nth-child(10) .infotext3 font')[0]).replace('<font size="2">', '').replace('</font>','')
    postcode = str(soup.select('tr:nth-child(11) .infotext3 font')[0]).replace('<font size="2">', '').replace('</font>','')
    website = ''
    try:
        website = str(soup.select('tr:nth-child(14) .infotext3 font a')[0]).split(' ')[1][6:-1]
    except:
        website = ''
    tel = str(soup.select('tr:nth-child(16) .infotext3 font')[0]).replace('<font size="2">', '').replace('</font>','')
    type = str(soup.select('tr:nth-child(18) .infotext3')[0]).replace('<td class="infotext3" height="22" valign="bottom">\n\t\t\t', '').replace('</td>','')
    if 'primary' in type:
        type = 'primary'
    elif 'secondary' in type:
        type = 'secondary'
    elif 'other' in type:
        type = 'other'
    elif 'independent' in type:
        type = 'independent'
    elif 'special' in type:
        type = 'special'
    return [school,street,town,county,postcode,website,tel,type]


def process_county(county,f):
    global jobs
    url = 'http://schoolswebdirectory.co.uk/index.php?county=%s&where=4&submit=Submit' % county.replace(' ','+')
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page,features='lxml')
    for link in soup.findAll('a'):
        if 'schoolinfo2.php?ref=' in link.get('href'):
            jobs.put(link.get('href'))

def top_level(url):
    global jobs
    f = csv.writer(open('schools.csv', 'w'))
    threading.Thread(target=worker, daemon=True, args=[f]).start()
    parser = etree.HTMLParser()
    data = requests.get(url, headers=headers, timeout=10).text
    tree = etree.parse(StringIO(data), parser=parser)
    counties = tree.xpath("//select")[0]
    for county in counties[1:]:
        process_county(county.text,f)
    jobs.join()
    f.close()


def get_emails():
    global jobs
    f = csv.writer(open('schools_final.csv', 'w'))
    entries = open('schools.csv', 'r').readlines()
    threading.Thread(target=worker2, daemon=True, args=[f]).start()
    for entry in entries:
        jobs.put(entry)
    jobs.join()


if __name__ == '__main__':
    get_emails()
