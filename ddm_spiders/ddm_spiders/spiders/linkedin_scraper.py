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
    'JSESSIONID': 'ajax:4339321431270984918',
    'bcookie': 'v=2&802fae70-c1ac-4263-8fe1-642d05122631',
    'bscookie': 'v=1&20191111195616302c7ee4-4d54-40be-8031-74da502ef491AQHmZysY-ozDtQO2hykEAvh1nGPEL5mh',
    'lidc': 'b=TB81:g=1969:u=7:i=1573502180:t=1573588580:s=AQGFu682Oq2rHJtQ1Qj42hgLWTNkioE3',
    'li_at': 'AQEDASrUviUDeZ4pAAABblwJ2tcAAAFugBZe100Azq9k4uwt3dSUiEpT0QI5H7tlRjiUBkHLXWuGJhDQP5xkwMZYiTZ-nDspqJ3Lppbiss4VWo9tg8_WhUyiaAty8zkfsOw9QXsF5gSLvo1RFP5ZEO2w',
    'liap': 'true',
    'sl': 'v=1&4EtMa',
    'lissc1': '1',
    'lissc2': '1',
    'lang': 'v=2&lang=en-us',
    '_lipt': 'CwEAAAFuXAnvjgqcDpGJm-WJ9DFWWEAiwW-4sZxwtY_Vu4NHWNMbKPVBXhF9XjaO-g5O2eOHi2fb9qUjdOYK4uZUpTQ11DC1n88GM8lHAk3TNpXW2_SWHzvOwXQPLiUDfVFBlnzo2gNkAY3rThqaUYhOkY3VkKP0t0bOrH0bTmh4Mgzmi-9BL5xbZtWMhhk7ScUGT1tb7Kz5lQGU3DQ0wToxJ6l3zHlKiawTFSo',
    'UserMatchHistory': 'AQKTo3L-_TNp_gAAAW5cCfYAROnphZTgyhtPc3byj0QuokDCpSNH3I_8sf16SeGNiRaezqXT3Tl36BzM6pXk6E3HC2CPNjkIwVLp1vJWsVfrmhf5AMdcMvXU_DljmrHz-I_3RLikdlipHcQ',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}

lkd_regex = re.compile(r'linkedin\.com\/(company|showcase|school)\/[^\/?"]*', re.IGNORECASE)
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

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
