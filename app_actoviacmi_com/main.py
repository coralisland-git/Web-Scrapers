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
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.encode('ascii', 'ignore').decode("utf-8").replace('~~', ', ').replace('~', ', ').strip()

def main():   
    session = requests.Session()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'removed',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    with open('output.csv', mode='w', newline="") as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['First name', 'Last name', 'Phone', 'Email', 'BBL'])
        idx = 0
        unit = 4000 
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
                    'Cookie': 'removed',
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
                emails = ', '.join(json.loads(email_response.text).get('List'))
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
                bbl_list = []
                for property in property_list:
                    bbl_list.append(property.get('BBL'))
                writer.writerow([
                    validate(owner.get('First')),
                    validate(owner.get('Last')),
                    validate(owner.get('AllPhones')),
                    emails,
                    ', '.join(bbl_list)
                ])                
                time.sleep(2)
            if idx*unit > 127547:
                break
            idx += 1

if __name__ == '__main__':
    main()
    