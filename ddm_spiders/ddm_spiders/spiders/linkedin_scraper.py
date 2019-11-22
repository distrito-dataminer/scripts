# -*- coding: utf-8 -*-
import scrapy
from collections import OrderedDict
import re
from unidecode import unidecode
from more_itertools import unique_everseen as unique
from urllib.parse import urlparse
import csv
import json
import pprint
import os
from datetime import datetime

cookies = {
    'bcookie': 'v=2&efa04615-f7bd-4354-8059-dfd6ed04652c',
    'bscookie': 'v=1&20181126132739da50067d-d328-4290-8041-abc247df16e2AQGwX8Q57D6Zj8vKyMBnhxn1_I2JOw2S',
    'JSESSIONID': 'ajax:9028902051245035064',
    'visit': 'v=1&M',
    '_lipt': 'CwEAAAFuji6Zb1HJF0cw8tWFEVuSP46eofI5s25Z2mciivmIwIbnt5sBIBUAyFD-m_5gO5IIgKyMkrKgX1IA81XdBW2PSlPltwd_Ilnlcqcx-LDZRbNkaxfDGLSCQ5KhMhEieLOrnlEWtOz1PPoA13eOq99SveJTr4BcOjxQt9-CLMpaKljZOj5_vapAGjTiXWfdC4oTw9T0sHNS-YJQhbjykSXaLwdUIg1zPg8BQNkNBkjYV93kHAfvvFmBB3sTDQjf0FfrcmPHzGEiB01uE8vwFjwM8AGmbdjbtAj6lacW6FRCRUf99unqFt0etTGjfTyLXWhu9OOyeYvWLWMwLUnNlSWJH1EvjjkOYUL_auBHhEp-3hcFB7RjIp8BKakprg_vXPi4APkhpJZsxxOFVOIZLVrsYFudn9Z_4vcpIzJJ-90vDOg_ns6qx0PKXjc6I9onnA',
    'org_tcphc': 'true',
    'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-1891778711%7CMCIDTS%7C18212%7CMCMID%7C91815213977225861640575468564591355059%7CMCOPTOUT-1573490739s%7CNONE%7CvVersion%7C2.4.0',
    'UserMatchHistory': 'AQKA6R1AGJoj2AAAAW6OLpuH-hDk7gcYkFb4-R8Bf_-z3gCivQnQa6lKEZAlV1_xEQuHez0GKuAjSGhwA7iui5bnhMSHkK_i7IHHjcVq5R79dTgVvpanP5DHcGwIihXyNo3EN8nfBU6-nOzYZlQ2wKeVOiDe5Oe8gAYlBjT-bvzcLkgv',
    'VID': 'V_2019_03_14_16_1004509',
    'utag_main': 'v_id:016a03d88eb7000f0d6316193d310004e00fe00d00bd0$_sn:3$_se:3$_ss:0$_st:1562880149903$vapi_domain:linkedin.com$ses_id:1562878260064%3Bexp-session$_pn:3%3Bexp-session',
    'sl': 'v=1&AhsxO',
    'liap': 'true',
    'li_at': 'AQEDARvom5kBHOHbAAABbn9pF88AAAFuo3Wbz00AiAASnEncSgoTs_xpxpNNpmIWh-RW7eUUJcL6H-9mZLDER1rfTV_NvBx5dqhFy15WDy3pzF3CEdwTXtAnxfvTZQrUH2L8QPrCtJDO-mjDg_SNMjHv',
    'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
    'sdsc': '22%3A1%2C1574173518014%7ECONN%2C01TXD8QuOaYSiSVbNnGgQQguQKsw%3D',
    'PLAY_SESSION': 'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiI5ZjUxYWQzYi0zMDQ0LTRkNjUtOGZiYi01MzA1MzJjZjBlMGJ8MTU3MTI1NTE3NCIsInJlY2VudGx5LXNlYXJjaGVkIjoiIiwicmVmZXJyYWwtdXJsIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJhaWQiOiIiLCJSTlQtaWQiOiJ8MCIsInJlY2VudGx5LXZpZXdlZCI6IjUwMjMwfDU5MzJ8MzQ1MzQiLCJDUFQtaWQiOiJNRGswTkRrd016SXRaVEV4WWkwMFpEaGxMV0ZsT0RNdE9HWTVZMk14Tmpka1pHWTIiLCJleHBlcmllbmNlIjoiZW50aXR5IiwiaXNfbmF0aXZlIjoiZmFsc2UiLCJ3aGl0ZWxpc3QiOiJ7fSIsInRyayI6IiJ9LCJuYmYiOjE1NzEyNTc4ODQsImlhdCI6MTU3MTI1Nzg4NH0.nWFNPw2mQ7bjvX0QRkAzbWvJpvQoh9JWf-NxMAGmxNE',
    'PLAY_LANG': 'en',
    'SID': 'bea422b5-2faa-4b89-811e-d7f6eafcdde8',
    'li_a': 'AQJ2PTEmY2FwX3NlYXQ9MTcwMTczNjIzJmNhcF9hZG1pbj1mYWxzZSZjYXBfa249MjQ0NDk4ODQxCkFAhmdM7KHk3lLqqFDC_ak1Jfg',
    'lissc1': '1',
    'lissc2': '1',
    'lang': 'v=2&lang=pt-br',
    'cap_session_id': '3044911093:1',
    'u_tz': 'GMT-03:00',
    'fid': 'AQHSJRrwnaclZAAAAW5_ahQk7g5XxzXqVwRLq_9zJSIwqRYtoWhHYMEQ-ztjUC2ib28yNrLRdA493A',
    'lidc': 'b=VB17:g=2884:u=336:i=1574342977:t=1574421527:s=AQFCYirY-pOfyPYS0gE7WlbQE93i-w_y',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
}

lkd_regex = re.compile(r'linkedin\.com\/(company|showcase|school)\/[^\/?"]*', re.IGNORECASE)
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

no_replace = False

class LkdSpider(scrapy.Spider):

    startup_list = []
    if 'lkddata.csv' in os.listdir('C:\\Test\\'):
        with open('C:\\Test\\lkddata.csv', 'r', encoding='utf8') as f:
            startup_csv = csv.DictReader(f)
            for startup in startup_csv:
                startup_list.append(startup)
            f.close()
            
#    startup_list = [{'LinkedIn': 'https://www.linkedin.com/company/stonosdc/'}]

    name = 'lkdscraper'
    allowed_domains = ['www.linkedin.com']
    
    def start_requests(self):
        if no_replace:
            urls = [startup['LinkedIn'] for startup in self.startup_list if startup['LinkedIn'] and startup['Nome LKD'] == '']
        else:
            urls = [startup['LinkedIn'] for startup in self.startup_list if startup['LinkedIn']]
        for url in urls:
            url_lkd = re.search(lkd_regex, url)
            if url_lkd:
                url = 'https://www.'+url_lkd.group()+'/'
            else:
                continue
            yield scrapy.Request(url = url, callback = self.parse, headers = headers, cookies = cookies)

    def parse(self, response):

        lkd_info = OrderedDict()
        lkd_info['timestamp'] = now
        lkd_info['url'] = response.request.url
        
        code_list = response.xpath('//code/text()').extract()
        code_list = [json.loads(n) for n in code_list if '{' in n]
        company_regex = re.compile(r'company:(\d+)')
        matches = re.findall(company_regex, response.text)

        match_dict = {}
        for match in matches:
            if match not in match_dict:
                match_dict[match] = 1
            else:
                match_dict[match] += 1

        max_value = 0
        for key, value in match_dict.items():
            if value > max_value:
                max_value = value
                lkd_id = key
                
        lkd_info['company_id'] = lkd_id

        company_info = {}

        for code in code_list:
            try:
                if lkd_id in code['data']['*elements'][0]:
                    if len(code['included']) > 1:
                        company_info = code['included']
            except:
                continue
            
        if not company_info:
            print('\n\n\n!!!Company info for {} not found!!!\n\n\n'.format(response.url))
        
        company_details = {}
                      
        biggest_item = 0

        for item in company_info:
            if '$type' in item and item['$type'] == 'com.linkedin.voyager.common.FollowingInfo':
                if 'entityUrn' in item and lkd_id in item['entityUrn']:
                    lkd_info['follower_count'] = item['followerCount']
            if '$type' in item and item['$type'] == 'com.linkedin.voyager.organization.Company':
                if len(item.keys()) > biggest_item:
                    biggest_item = len(item.keys())
                    company_details = item
        
        if company_details:
            lkd_info['name'] = company_details.get('name')
            lkd_info['staff_count'] = company_details.get('staffCount')
            foundedOn = company_details.get('foundedOn')
            if foundedOn:
                lkd_info['founded_year'] = foundedOn.get('year')
            lkd_info['description'] = company_details.get('description')
            lkd_info['employee_search_page_url'] = company_details.get('companyEmployeesSearchPageUrl')
            phone = company_details.get('phone')
            if phone:
                lkd_info['phone'] = phone.get('number')
            lkd_info['tagline'] = company_details.get('tagline')
            headquarter = company_details.get('headquarter')
            if headquarter:
                lkd_info['headquarter'] = company_details.get('headquarter')
                lkd_info['city'] = headquarter.get('city')
                lkd_info['geographic_area'] = headquarter.get('geographicArea')
                lkd_info['country'] = headquarter.get('country')
            logo = company_details.get('logo')
            if logo:
                logo_image = logo.get('image')
                if logo_image:
                    root_url = logo_image.get('rootUrl')
                    artifacts = logo_image.get('artifacts')
                    biggest_logo_url = None
                    if type(artifacts) == list:
                        biggest_logo_url = artifacts[-1].get('fileIdentifyingUrlPathSegment')
                    elif type(artifacts) == dict:
                        biggest_logo_url = artifacts.get('fileIdentifyingUrlPathSegment')
                    if biggest_logo_url:
                        lkd_info['logo_url'] = root_url + biggest_logo_url
            tags = company_details.get('specialities')
            if type(tags) == list:
                lkd_info['tags'] = ','.join(tags)
            lkd_info['universal_name'] = company_details.get('universalName')
            lkd_info['website'] = company_details.get('companyPageUrl')
            lkd_info['standard_url'] = company_details.get('url')
            lkd_info['auto_generated'] = company_details.get('autoGenerated')
            lkd_info['showcase'] = company_details.get('showcase')
            staff_range = company_details.get('staffCountRange')
            if staff_range:
                lkd_info['staff_range'] = '{}-{}'.format(staff_range.get('start'), staff_range.get('end'))
            lkd_info['confirmed_locations'] = company_details.get('confirmedLocations')
            lkd_info['paid_company'] = company_details.get('paidCompany')
            companyType = company_details.get('companyType')
            if companyType:
                lkd_info['company_type'] = companyType.get('code')
        
        yield lkd_info
