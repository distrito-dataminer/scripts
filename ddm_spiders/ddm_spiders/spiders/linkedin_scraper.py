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
    'JSESSIONID': 'ajax:9147326614135056356',
    'bcookie': 'v=2&64ad6a58-c268-414e-83ad-5107bc5242da',
    'bscookie': 'v=1&20191119220446fd7fc5a5-78a5-483c-80d3-6b74765057b8AQHI7J0qHd9jRH4NhL-LJA09EDTsTn7F',
    'lidc': 'b=TB81:g=1980:u=7:i=1574201089:t=1574287489:s=AQFreBXw1_fAR8f0P2FzxKkbx7oGzwST',
    'sl': 'v=1&GJwiM',
    'liap': 'true',
    'li_at': 'AQEDASrUviUCuTzeAAABboWyXEkAAAFuqb7gSU4Abap7HjoPqzasZ607ia8vtzYyv_2oe0s0774WZOe6AyHM-GCh3Aj2PfZESLOFRms-FG4_62m6FJnm2COq8Dea47lm1gxJ0xbrUe4jfK20I6qA_3JJ',
    'lissc1': '1',
    'lissc2': '1',
    'lang': 'v=2&lang=en-us',
    '_lipt': 'CwEAAAFuhbJkiELd0uDAYMtVLCCoLEEwxu7W28gGlJKvg_5e5E-c_VvM7S2q7fcdEQ4mnlbyzvsAVnUR9gPCTUpAdb7f618W4Fg3GW-1di_8HPav7nXiO5SZLnxBH-RKbD1rzWr8DRNSj1oHKi8JIhdNvevKiZdkGsRFj37WQ4QupG7jY_mX-peTWSytoybx7qnU3NW-O6AMI54wRCEy91hk1SYKSso7_w',
    'UserMatchHistory': 'AQIMTtiwxXq_igAAAW6FspdSXE0VGDrEWo-O9gfrl0BB2BVupF3ALhGxOLAFaGeozRVXqxrpQdxgTjoPe9Yn8BlUFowXrYa84rnJYdEUFaGON2lKjQsN6h-qoRxrqSydkVLdQ9K34FEG2QQ',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'DNT': '1',
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
