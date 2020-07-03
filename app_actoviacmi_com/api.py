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
from closeio_api import Client


api = Client('api_5ivDk55sUEI1C3YPxl0Agy.0SigTV6fgVIRLXXEkJyQ95')

def validate(item):
    if item == None:
        item = ''
    if type(item) == bool:
        return item
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').decode("utf-8").replace('~~', ',').replace('~', ',').strip()

def format(item):
    if item == '':
        return None
    return item

def main():   
    session = requests.Session()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': '_ga=GA1.2.714347873.1591899550; property=id=MT8GOD529F; G_ENABLED_IDPS=google; _ga=GA1.3.714347873.1591899550; ASP.NET_SessionId=th1j0p4asknie0baszrhf0wp; _gid=GA1.2.1687458424.1593617714; acmiappaddressplaceholder_nyc=addressplaceholder=Search Address (eg: 123 Brook Ave, Bronx); acmiappbblplaceholder_nyc=bblplaceholder=search BBL (eg: M-1234-12) enter M-Manhattan, B-Bronx, K-Brooklyn, Q-Queens; _gid=GA1.3.1687458424.1593617714; acmiapp_7days=JfK8T97LZLyFqXxwO-EKpGLsPVBeV8_Amm3RDrr1WVSEb8m32jX6AUE0E1ZAOHxuWdQvn7b-h-9gsUb-UsDCyQ,,; _gat_UA-90222469-2=1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }        
    idx = 0
    unit = 4000
    output_list = []
    filter_by_zipcode = input("zipcode:")
    limit = input("limit:")
    try:
        limit = int(limit)
    except:
        print('Invalid format')
        limit = 0
    exist_count = 0
    new_count = 0
    file_name = 'output.json'
    if filter_by_zipcode != '':
        file_name = filter_by_zipcode + '-' + file_name

    try:
        with open(file_name) as data_file:
            output_list = json.load(data_file)
        exist_count = len(output_list)
    except:
        pass

    while True:
        start = exist_count + new_count
        owner_url = 'https://app.actoviacmi.com/Owners/GetList'
        owner_payload = {
            "draw": 1,
            "columns": [
                {
                    "data": "Id",
                    "name": "",
                    "searchable": True,
                    "mycustomfield": None,
                    "orderable": True,
                    "search": {
                        "value": "",
                        "regex": False
                    }
                },
                {
                    "data": "First",
                    "name": "",
                    "searchable": True,
                    "mycustomfield": None,
                    "orderable": True,
                    "search": {
                        "value": "",
                        "regex": False
                    }
                },
                {
                    "data": "Last",
                    "name": "",
                    "searchable": True,
                    "mycustomfield": None,
                    "orderable": True,
                    "search": {
                        "value": "",
                        "regex": False
                    }
                },
                {
                    "data": "FullName",
                    "name": "",
                    "searchable": True,
                    "mycustomfield": None,
                    "orderable": True,
                    "search": {
                        "value": "",
                        "regex": False
                    }
                },
                {
                    "data": "NrInCurrent",
                    "name": "",
                    "searchable": True,
                    "mycustomfield": None,
                    "orderable": True,
                    "search": {
                        "value": "",
                        "regex": False
                    }
                },
                {
                    "data": "NrProperties",
                    "name": "",
                    "searchable": True,
                    "mycustomfield": None,
                    "orderable": True,
                    "search": {
                        "value": "",
                        "regex": False
                    }
                },
                {
                    "data": "IsProspect",
                    "name": "",
                    "searchable": True,
                    "mycustomfield": None,
                    "orderable": False,
                    "search": {
                        "value": "",
                        "regex": False
                    }
                }
            ],
            "order": [
                {
                  "column": 5,
                  "dir": "desc"
                }
            ],
            "start": start,
            "length": unit,
            "search": {
            "value": "",
                "regex": False
            },
            "type": "a",
            "bbl": "",
            "askingPrice": "",
            "years": -5,
            "variation": 15,
            "search1": "",
            "sid": "",
            "stage": ""
        }
        owner_response = session.post(owner_url, headers=headers, data=json.dumps(owner_payload))
        owner_list = json.loads(owner_response.text).get('data')
        for owner in owner_list:
            if limit != 0 and new_count >= limit:
                break
            email_url = 'https://app.actoviacmi.com/Owners/GetEmailsByOwnerId'
            email_headers = {
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': '_ga=GA1.2.714347873.1591899550; property=id=MT8GOD529F; G_ENABLED_IDPS=google; _ga=GA1.3.714347873.1591899550; ASP.NET_SessionId=th1j0p4asknie0baszrhf0wp; _gid=GA1.2.1687458424.1593617714; acmiappaddressplaceholder_nyc=addressplaceholder=Search Address (eg: 123 Brook Ave, Bronx); acmiappbblplaceholder_nyc=bblplaceholder=search BBL (eg: M-1234-12) enter M-Manhattan, B-Bronx, K-Brooklyn, Q-Queens; _gid=GA1.3.1687458424.1593617714; acmiapp_7days=JfK8T97LZLyFqXxwO-EKpGLsPVBeV8_Amm3RDrr1WVSEb8m32jX6AUE0E1ZAOHxuWdQvn7b-h-9gsUb-UsDCyQ,,; _gat_UA-90222469-2=1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            email_response = session.post(
                email_url, 
                headers=email_headers, 
                data={
                    'ownerid': validate(owner.get('Id'))
                }
            )
            emails = json.loads(email_response.text).get('List')
            property_url = 'https://app.actoviacmi.com/_Properties/GetList'
            property_payload = {
                "draw": 1,
                "columns": [
                    {
                        "data": 0,
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": False,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "OwnNote",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                          "value": "",
                          "regex": False
                        }
                    },
                    {
                        "data": "IsStar",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                          "value": "",
                          "regex": False
                        }
                    },
                    {
                        "data": "ProspectStatus",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "NrNotes",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "BBL",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "proptype.propertytype",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "StreetNumber",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "StreetName",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "City",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "County",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "State",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "Zip",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "BuildingClass",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "Stories",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "Units",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "IsCondo",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "sq_ft",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "l.name",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "morgAmount",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "MorgDateRecorded",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "MorgExpirationDate",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "PrepayPenalty",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "RatePPPChgate",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "Cap_Rate",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "MorgDateActual",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "morgRate",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "isForclosure",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "LoanToValue",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "isMortgagePaid",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "DeedDateRecorded",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "DeedDateActual",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "DeedAmount",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "IsPackage",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "DeedAmount/Noneif(p.Units,0)",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "morgAmount/Noneif(p.Units,0)",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "morgAmount/Noneif(p.sq_ft,0)",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "DeedAmount/Noneif(p.sq_ft,0)",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "IsInConstruction",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "construction_stage",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "occpercentage",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "IsLandmark",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "year_built",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "Year_renovated_1",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "Year_renovated_2",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "j.name",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "j.indicator",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "jm.judgemaxamt",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                          "value": "",
                          "regex": False
                        }
                    },
                    {
                        "data": "jm.judgemaxdate",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "z.name",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "isNone(p.lotsize, p.lotfront*p.lotdepth)",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "lt.name",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "FAR",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "far*isNone(p.lotsize, p.lotfront*p.lotdepth)-isNone(p.sq_ft,0)",
                        "name": "",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    },
                    {
                        "data": "Id",
                        "name": "id_property",
                        "searchable": True,
                        "mycustomfield": None,
                        "orderable": True,
                        "search": {
                            "value": "",
                            "regex": False
                        }
                    }
                ],
                "order": [],
                "start": 0,
                "length": 1000,
                "search": "",
                "type": "",
                "ownerid": validate(owner.get('Id')),
                "currentSearch": False,
                "searchId": -1,
                "filters": [],
                "statistics": [],
                "stage": ""
            }
            property_response = session.post(
                property_url, 
                headers=headers,
                data=json.dumps(property_payload)
            )            
            property_list = json.loads(property_response.text).get('data')            
            pp_list = []
            for property in property_list:
                if filter_by_zipcode != '' and filter_by_zipcode != validate(property.get('Zip')):
                    continue
                contacts = []
                for key, value in property.items():
                    if 'Contact' in key and validate(property.get(key).get('Email')) != '':
                        contacts.append({
                            'name': '{} {}'.format(validate(property.get(key).get('First')), validate(property.get(key).get('Last'))),
                            'title': validate(property.get(key).get('BusinessName')),
                            'emails': [
                                {
                                    'type': 'office',
                                    'email': validate(property.get(key).get('Email'))
                                }
                            ],
                            'phones': [
                                {
                                    'type': 'office',
                                    'phone': validate(property.get(key).get('Phone1'))
                                }
                            ]
                        })
                # if len(contacts) == 0:
                #     continue
                custom = {
                        'neighborhood': format(property.get('City')),

                        'type': format(property.get('Type')),
                        'buildingClass': format(property.get('BuildingClass')),
                        'taxClass': format(property.get('TaxClass')),
                        'units': format(property.get('Units')),
                        'stories': format(property.get('Stories')),
                        'sqFt': format(property.get('SqFt')),

                        'isInConstruction': format(property.get('IsInConstruction')),
                        'constructionStage': format(property.get('ConstructionStage')),
                        'yearBuilt': format(property.get('YearBuilt')),
                        'yearMod1': format(property.get('YearMod1')),
                        'yearMod2': format(property.get('YearMod2')),

                        'zoning': format(property.get('Zoning')),
                        'lotType': format(property.get('LotType')),
                        'lotSize': format(property.get('LotSize')),
                        'floorAreaRatio': format(property.get('FAR')),
                        'airRights': format(property.get('AvailableSqFt')),

                        'grossIncome': format(property.get('Income')),
                        'grossExpense': format(property.get('Expense')),
                        'noi': format(property.get('Income') - property.get('Expense')),
                        'opportunityZone': format(property.get('OppZone')),

                        'isCondo': format(property.get('IsCondo')),
                        'isCityOwned': format(property.get('IsCityOwned')),
                        'isLandmark': format(property.get('IsLandmark')),

                        'lender': format(property.get('Lender')),
                        'mtgeAmount': format(property.get('MtgeAmount')),
                        'mtgeDateActual': format(property.get('MtgeDateActual')),
                        'mtgeDateRec': format(property.get('MtgeDateRec')),
                        'mtgeExpiration': format(property.get('MtgeExpiration')),

                        'interestRate': format(property.get('MtgeRate')),
                        'prepayPenalty': format(property.get('PrepayPenalty')),
                        'isMtgePaid': format(property.get('IsMtgePaid')),

                        'isPurchase': format(property.get('IsPurchase')),
                        'potentialSale': format(property.get('PotentialSale')),
                        'loanToValue': format(property.get('LoanToValue')),
                        'capRate': format(property.get('CapRate')),

                        'saleAmount': format(property.get('DeedAmount')),
                        'fullVal': format(property.get('FullVal')),
                        'saleDateRec': format(property.get('DeedDateRec')),
                        'saleDateActual': format(property.get('DeedDateActual')),

                        'mtgePrcPerUnit': format(property.get('MtgePrcPerUnit')),
                        'mtgePrcPerSqFt': format(property.get('MtgePrcPerSqFt')),
                        'deedPrcPerUnit': format(property.get('DeedPrcPerUnit')),
                        'deedPrcPerSqFt': format(property.get('DeedPrcPerSqFt')),

                        'lienType': format(property.get('JudgementType')),
                        'lienDetails': format(property.get('JudgementInd'))
                    }

                empty_keys = []

                for key, value in custom.items():
                    if value == '' or value == None:
                        empty_keys.append(key)

                for e_key in empty_keys:
                    del custom[e_key]

                data = {
                    'name': format(property.get('BBL')),
                    'contacts': contacts,
                    'addresses': [
                        {
                            'label': 'business',
                            'address_1': format(validate(property.get('Address'))),
                            'address_2': '',
                            'city': format(property.get('County')),
                            'state': format(property.get('State')),
                            'zipcode': format(property.get('Zip')),
                            'country':'US',
                        }
                    ],
                    'custom' : custom
                    
                }
                lead = api.post('lead', data=data)
                print(data['name'])
            new_count += 1
            time.sleep(1)
               
        if idx*unit > 127547 or (limit != 0 and new_count >= limit):
            break
        idx += 1        


if __name__ == '__main__':
    main()
