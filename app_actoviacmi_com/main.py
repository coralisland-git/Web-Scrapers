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

def main():   
    session = requests.Session()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': '_ga=GA1.2.714347873.1591899550; ASP.NET_SessionId=dhpzzpbjukkcssv0pqlfzlhu; property=id=MT8GOD529F; G_ENABLED_IDPS=google; _ga=GA1.3.714347873.1591899550; _gid=GA1.2.1677424999.1592241404; acmiapp_7days=JfK8T97LZLyFqXxwO-EKpGLsPVBeV8_Amm3RDrr1WVSEb8m32jX6AUE0E1ZAOHxuWdQvn7b-h-9gsUb-UsDCyQ,,; acmiappaddressplaceholder_nyc=addressplaceholder=Search Address (eg: 123 Brook Ave, Bronx); acmiappbblplaceholder_nyc=bblplaceholder=search BBL (eg: M-1234-12) enter M-Manhattan, B-Bronx, K-Brooklyn, Q-Queens; _gid=GA1.3.1677424999.1592241404; _gat_UA-90222469-2=1',
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
        print('invalid format')
        limit = 0    
    file_name = 'output.json'
    if filter_by_zipcode != '':
        file_name = filter_by_zipcode + '-' + file_name
    while True:
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
            "start": unit*idx,
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
            email_url = 'https://app.actoviacmi.com/Owners/GetEmailsByOwnerId'
            email_headers = {
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': '_ga=GA1.2.714347873.1591899550; ASP.NET_SessionId=dhpzzpbjukkcssv0pqlfzlhu; property=id=MT8GOD529F; G_ENABLED_IDPS=google; _ga=GA1.3.714347873.1591899550; _gid=GA1.2.1677424999.1592241404; acmiapp_7days=JfK8T97LZLyFqXxwO-EKpGLsPVBeV8_Amm3RDrr1WVSEb8m32jX6AUE0E1ZAOHxuWdQvn7b-h-9gsUb-UsDCyQ,,; acmiappaddressplaceholder_nyc=addressplaceholder=Search Address (eg: 123 Brook Ave, Bronx); acmiappbblplaceholder_nyc=bblplaceholder=search BBL (eg: M-1234-12) enter M-Manhattan, B-Bronx, K-Brooklyn, Q-Queens; _gid=GA1.3.1677424999.1592241404; _gat_UA-90222469-2=1',
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
                pp = {
                    'Address': validate(property.get('Address')),
                    'Contacts': [
                        {
                            'FirstName': validate(property.get('Contact2').get('First')),
                            'LastName': validate(property.get('Contact2').get('Last')),
                            'Phone': validate(property.get('Contact2').get('Phone1')),
                            'Email': validate(property.get('Contact2').get('Email')),
                            'BusinessName': validate(property.get('Contact2').get('BusinessName')),
                            'AppDate': validate(property.get('Contact2').get('AppDate')),
                        },
                        {
                            'FirstName': validate(property.get('Contact3').get('First')),
                            'LastName': validate(property.get('Contact3').get('Last')),
                            'Phone': validate(property.get('Contact3').get('Phone1')),
                            'Email': validate(property.get('Contact3').get('Email')),
                            'BusinessName': validate(property.get('Contact3').get('BusinessName')),
                            'AppDate': validate(property.get('Contact3').get('AppDate')),
                        }
                    ],

                    'BBL': validate(property.get('BBL')),
                    'Neighborhood': validate(property.get('City')),
                    'Boro': validate(property.get('County')),
                    'Zipcode': validate(property.get('Zip')),

                    'Type': validate(property.get('Type')),
                    'BuildingClass': validate(property.get('BuildingClass')),
                    'TaxClass': validate(property.get('TaxClass')),
                    'Units': validate(property.get('Units')),
                    'Stories': validate(property.get('Stories')),
                    'SqFt': validate(property.get('SqFt')),

                    'IsInConstruction': validate(property.get('IsInConstruction')),
                    'ConstructionStage': validate(property.get('ConstructionStage')),
                    'YearBuilt': validate(property.get('YearBuilt')),
                    'YearMod1': validate(property.get('YearMod1')),
                    'YearMod2': validate(property.get('YearMod2')),

                    'Zoning': validate(property.get('Zoning')),
                    'LotType': validate(property.get('LotType')),
                    'LotSize': validate(property.get('LotSize')),
                    'FloorAreaRatio': validate(property.get('FAR')),
                    'AirRights': validate(property.get('AvailableSqFt')),

                    'GrossIncome': validate(property.get('Income')),
                    'GrossExpense': validate(property.get('Expense')),
                    'NOI': validate(property.get('Income') - property.get('Expense')),
                    'OpportunityZone': validate(property.get('OppZone')),

                    'IsCondo': validate(property.get('IsCondo')),
                    'IsCityOwned': validate(property.get('IsCityOwned')),
                    'IsLandmark': validate(property.get('IsLandmark')),                    

                    'Lender': validate(property.get('Lender')),
                    'MtgeAmount': validate(property.get('MtgeAmount')),
                    'MtgeDateActual': validate(property.get('MtgeDateActual')),
                    'MtgeDateRec': validate(property.get('MtgeDateRec')),
                    'MtgeExpiration': validate(property.get('MtgeExpiration')),

                    'InterestRate': validate(property.get('MtgeRate')),
                    'PrepayPenalty': validate(property.get('PrepayPenalty')),                    
                    'IsMtgePaid': validate(property.get('IsMtgePaid')),

                    'IsPurchase': validate(property.get('IsPurchase')),
                    'PotentialSale': validate(property.get('PotentialSale')),
                    'LoanToValue': validate(property.get('LoanToValue')),
                    'CapRate': validate(property.get('CapRate')),

                    'SaleAmount': validate(property.get('DeedAmount')),
                    'FullVal': validate(property.get('FullVal')),
                    'SaleDateRec': validate(property.get('DeedDateRec')),
                    'SaleDateActual': validate(property.get('DeedDateActual')),                    

                    'MtgePrcPerUnit': validate(property.get('MtgePrcPerUnit')),
                    'MtgePrcPerSqFt': validate(property.get('MtgePrcPerSqFt')),
                    'DeedPrcPerUnit': validate(property.get('DeedPrcPerUnit')),
                    'DeedPrcPerSqFt': validate(property.get('DeedPrcPerSqFt')),

                    'LienType': validate(property.get('JudgementType')),
                    'LienDetails': validate(property.get('JudgementInd')),                    
                }
                pp_list.append(pp)
            output = {
                'Id': validate(owner.get('Id')),
                'FirstName': validate(owner.get('First')),
                'LastName': validate(owner.get('Last')),
                'Phone': validate(owner.get('AllPhones')).split(','),
                'Email': emails,
                'Properties': pp_list
            }
            if limit != 0 and len(output_list) >= limit:
                break
            output_list.append(output)
            print(output['FirstName'] + ' ' + output['LastName'])
            time.sleep(1)
            with open(file_name, mode='w') as output_file:
                data = json.dumps(output_list, sort_keys=True, indent=4)
                output_file.write(data)

        if idx*unit > 127547 or (limit != 0 and limit < idx*unit):
            break
        idx += 1        


if __name__ == '__main__':
    main()
    