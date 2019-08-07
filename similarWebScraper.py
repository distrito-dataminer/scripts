#! python3
# similarWebScraper.py - Scrapes SimilarWeb 

import sys
import json
import requests
import csv
import scrapy
import re

from time import sleep

from scrapy import Selector
from urllib.parse import urljoin

from utils import ddmdata, cleaner

cookies = {
    'D_SID': '179.191.65.154:arRz8n+aeVFopwH1SCV8rlNBFJUxQeKsnTZsvHn4Lu0',
    'locale': 'pt-BR',
    '.AspNetCore.Antiforgery.xd9Q-ZnrZJo': 'CfDJ8P7q8u2iyLhHnGjyS00LkJqxfiy5JzRC5-r801H0wEKfVMFl9vJ3cbJ7LOXz3hmpyeTycLRjtGAZKQHy9VgqCoj1MOFiSuQeL8asOgdvJVy2D6I5KHQenvPl6zNYYPoeNqL9iGkJ6eOIIYdRrx_eBJk',
    '_ga': 'GA1.2.589869296.1564768340',
    '_gid': 'GA1.2.200404949.1564768340',
    '_gcl_au': '1.1.1844985424.1564768340',
    'user_num': 'nowset',
    'sgID': 'd9705915-5c0c-5337-ed8c-194fbbf58bf7',
    '_vwo_uuid_v2': 'D728AFD0C48AF18A1959D1010C9DB67CE|e42fb45ccd09927b7c543e8dea615e3e',
    '_pk_ses.1.fd33': '*',
    'loyal-user': '{%22date%22:%222019-08-02T17:52:20.237Z%22%2C%22isLoyal%22:false}',
    '_gat': '1',
    'sc_is_visitor_unique': 'rx8617147.1564768340.18AB12D836B84F7AF55A2B3ED5019189.1.1.1.1.1.1.1.1.1',
    '_fbp': 'fb.1.1564768345079.931471164',
    '_hjid': '71b5e257-6c3d-4484-823f-36b95a76ec50',
    'visitor_id597341': '388070933',
    'visitor_id597341-hash': 'f34b334ba6eb4e96dff91de0f2f8179442b6cbf975321d89ccf441652c96aa645306c3be95e5c3d1d66dda1ab162cc4161929cba',
    'intercom-id-e74067abd037cecbecb0662854f02aee12139f95': '35b25117-12a9-4baa-ac97-415d77d8db2e',
    'D_IID': 'CEDEEF9E-E490-3958-9AB1-F16E1A200BD7',
    'D_UID': '4F91E75A-FFEC-3CE1-88AA-3D7CD735C189',
    'D_ZID': '0F2D9816-18F4-3A60-93C0-A9FE69AF64BC',
    'D_ZUID': '247F9808-8476-32F3-8ED7-DA1F07F924D0',
    'D_HID': '6D4CA1D4-952B-34BC-B0AD-DAB39B9B74CC',
    '_pk_id.1.fd33': 'e7f2332827a03187.1564768340.1.1564768350.1564768340.',
    'mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel': '%7B%22distinct_id%22%3A%20%2216c53760889636-0038e2617021ea-c343162-100200-16c5376088a713%22%2C%22%24device_id%22%3A%20%2216c53760889636-0038e2617021ea-c343162-100200-16c5376088a713%22%2C%22%24initial_referrer%22%3A%20%22http%3A%2F%2Fwww.similarweb.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.similarweb.com%22%2C%22sgId%22%3A%20%22d9705915-5c0c-5337-ed8c-194fbbf58bf7%22%2C%22site_type%22%3A%20%22Corp%22%2C%22session_id%22%3A%20%229d17bbd7-a6ee-45fd-b967-58b5553a148c%22%2C%22session_first_event_time%22%3A%20%222019-08-02T17%3A52%3A20.149Z%22%2C%22url%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fpt%22%2C%22is_sw_user%22%3A%20false%2C%22language%22%3A%20%22pt%22%2C%22section%22%3A%20%22home%22%2C%22first_time_visitor%22%3A%20true%2C%22last_event_time%22%3A%201564768349738%7D',
    '_gali': 'js-swSearch-input',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

startupList = ddmdata.readcsv(sys.argv[1])

results = []

for startup in startupList:
    if startup['Site']:
        swUrl = 'https://www.similarweb.com/pt/website/' + startup['Site'].replace('http://', '') + '#overview'

        print('Requesting {}...'.format(swUrl))

        try:
            response = requests.get(swUrl, headers=headers, cookies=cookies)
        except Exception as e:
            print(repr(e))
            continue

        if response.status_code != 200:
            print('Bad status. Status code: {}.'.format(response.status_code))
            continue

        raw_text = response.content
        print(raw_text)

        html_response = Selector(text=raw_text)

        swInfo = html_response.xpath('//*[@class = "engagementInfo-valueNumber js-countValue"]/text()').extract()

        if not swInfo:
            print("Couldn't get swinfo for {}.".format(startup['Site']))
            continue

        profile_details = {'Site': startup['Site'], 'SimilarWeb': swUrl}

        if len(swInfo) == 4:
            profile_details['totalVisits'] = swInfo[0]
            profile_details['timeSpent'] = swInfo[1]
            profile_details['pagesPerVisit'] = swInfo[2]
            profile_details['bounceRate'] = swInfo[3]
        else:
            print("swInfo for {} had a different length than expected. Length: {}".format(profile_details['Site'], str(len(swInfo))))

        results.append(profile_details)

ddmdata.writecsv(results, sys.argv[1].replace('.csv','')+'_similarWeb.csv')