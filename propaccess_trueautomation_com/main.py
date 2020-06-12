import csv
import re
import pdb
import requests
from lxml import etree
import json


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


def send_users_from_csv():    
    ids = []
    with open('input.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for idx, row in enumerate(spamreader):
            if idx != 0:
                ids.append(validate(row[2]))
    return ids


def write_output(data):
    with open('data.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["PropertyState", "PropertyCounty", "PropertyId", "OwnerName", "OwnerAddress", 
            "OwnerCity", "OwnterState", "OwnerZip", "LegalDescription", "Acres","% Ownership:"])
        for row in data:
            writer.writerow(row)


def fetch_data():
    ids = send_users_from_csv()
    output_list = []
    session = requests.Session()
    for id in ids:
        try:
            url = "https://propaccess.trueautomation.com/clientdb/Property.aspx?cid=39&prop_id={}".format(id)
            source = session.get(url).text
            response = etree.HTML(source)
            tds = response.xpath('//table[@summary="Property Details"]//td')
            for idx, td in enumerate(tds):
                if idx+1 >= len(tds):
                    break
                key = validate(td.xpath('.//text()'))
                value = eliminate_space(tds[idx+1].xpath('.//text()'))
                if 'Name:' == key:
                    name = validate(value)
                if 'Mailing Address:' == key:
                    try:
                        address = validate(value[:-1])
                        csz = eliminate_space(value[-1].split(','))
                        city = csz[0]
                        state = csz[1].split(' ')[0]
                        zipcode = csz[1].split(' ')[1]
                    except Exception as e:
                        print(e, address)
                        pdb.set_trace()
                if 'Legal Description:' == key:
                    description = validate(value)
                if '% Ownership:' == key:
                    ownership = validate(value)
            try:
                acres = eliminate_space(response.xpath('//table[@summary="Land Details"]//tr')[-1].xpath('.//text()'))[3]
            except:
                pass
            output = [
                "Texas", 
                "Aransas", 
                id,
                name,
                address,
                city,
                state,
                zipcode,
                description,
                acres,
                ownership
            ]            
            output_list.append(output)
        except Exception as e:
            print(e)
            pdb.set_trace()
    return output_list


def main():
    data = fetch_data()
    write_output(data)


if __name__ == '__main__':
    main()
