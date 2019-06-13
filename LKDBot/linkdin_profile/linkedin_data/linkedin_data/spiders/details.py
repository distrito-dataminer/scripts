# -*- coding: utf-8 -*-

import json
import requests
import csv
import scrapy

from scrapy import Selector
from urllib.parse import urljoin


class LinkedinData(scrapy.Spider):
    name = "lkdcrawler"
    start_urls = ['https://www.linkedin.com/']
    allowed_domains = ["www.linkedin.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }

    def parse(self, response):
        profiles = []
        f = open(r'C:\test\data.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['LinkedIn']
            if 'linkedin.com/' in url:
                profiles.append(url)
        for profile in profiles:

            url = urljoin(self.start_urls[0], profile.split('.com/')[1])
            
            cookies = {
                'JSESSIONID': 'ajax:2890114038180365552',
                'bcookie': 'v=2&cd8c7d73-88d7-4892-8597-6fe9a7868e0e',
                'bscookie': 'v=1&201906122035156daa49a8-e445-4449-8ba2-2e524cdbafe0AQHBZgfG1W127TDlPWTSBJ29TPq3CYhT',
                'lidc': 'b=VB17:g=2550:u=144:i=1560371724:t=1560425735:s=AQHqXgT6VzulexBDKGr7cY9udls-Ro-t',
                'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-1303530583%7CMCIDTS%7C18060%7CMCMID%7C12753094641755470479210125786293104177%7CMCOPTOUT-1560378917s%7CNONE%7CvVersion%7C3.3.0',
                'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
                'liap': 'true',
                'sl': 'v=1&k1KNo',
                'li_at': 'AQEDARvom5kB55EMAAABa01nAMAAAAFrcXOEwE4AqIMkrRSabec-BJDg1sAeUoXPlUOI2135QIinZ6_O3pnozM2GMONmD101JyhfC0HGbm3FXnA8-sMkirmuPI0D9oH5WfPPUBhQkvtoTizYKKXKfzUN',
                'lissc1': '1',
                'lissc2': '1',
                'lang': 'v=2&lang=pt-br',
                '_lipt': 'CwEAAAFrTWcIcyzZxlODryuE-IDUoR10JL09-frWrlJT2iECtO75OLLreMRPlWDWcmZwexdkorxV4TdoH1Bp__wZkm37yrttWwCi1PJVXVcb7eMuyjQqEphd32x7_LbGW5-rbMyEO492dFpxI0lwAPsFiiYVcwvj4jPz-MNRnztJfg7H0TP_xTdSTytjz5_zzS-cn2wJzHfkTUZwoDob8Z6VwuMuayvPRhP1lTpNVskbY3whFwc5ZOMIqMS-P28vF-qbAol_RnNO5Wwz-PbjtPj3DqXn8us4K6xKq9LFkt6woLU1Iufdp6P4izMnm5Zwod1n08paIx_sxVNhuK5Q3CKtHG-2xg_pH9CATlQrD4c2fNlzLa1rzO2ohA',
                'UserMatchHistory': 'AQKQJ1IcNutPXAAAAWtNZw-6aoqepXLVaAe7kgMg3jyiFGF3IIg8FexeBjWYDzFXby_PHcYy34-ZORiv0dyuIR6-Ai7P9p5iRS_CR-pmri0cDA',
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'TE': 'Trailers',
            }

            raw_text = requests.get(url, headers=headers, cookies=cookies)

            response = raw_text.content
            html_response = Selector(text=response)

            raw_details = html_response.xpath(
                '//*[contains(text(),"backgroundCoverImage")]/text()').extract_first()

            if not raw_details:
                continue

            details = json.loads(raw_details)
            profile_details = {}

            profile_detail = details['included']
            details_text = self.raw_details(profile_detail)

            if not details_text:
                continue

            detail = details_text[0]
            count = self.follower_count(profile_detail)

            name = detail.get('name')
            description = detail.get('description')
            website = detail.get('callToAction')
            staff_range = detail.get('staffCountRange')
            founded_year = detail.get('foundedOn')
            cover_image = detail.get('backgroundCoverImage')
            self_declared_employees = detail.get('staffCount')
            locations = detail.get('confirmedLocations')
            market = details.get('included')
            tags = detail.get('specialities')
            logo = detail.get('logo')

            if url:
                profile_details['url'] = url.replace("https://www.", "http://")

            if logo:
                raw_key = logo.get('image')
                logo_image = raw_key.get('artifacts')
                if logo_image:
                    key = logo_image[-1].get('fileIdentifyingUrlPathSegment')
                    profile_details['logo'] = f"{logo['image']['rootUrl']}{key}"

            if count:
                profile_details['follower_count'] = count[0]

            if name:
                profile_details['name'] = name

            if description:
                profile_details['description'] = description

            if website:
                profile_details['website'] = website.get('url')

            if staff_range:
                profile_details['company_size'] = f'{staff_range.get("start", "")} - {staff_range.get("end", "")}'

            if founded_year:
                profile_details['founded_year'] = founded_year.get('year')

            if cover_image:
                image = cover_image.get('image')
                if image:
                    raw_image = image.get('artifacts')
                    if raw_image:
                        profile_details['cover_image'] = raw_image[0].get(
                            'fileIdentifyingUrlPathSegment')
            else:
                profile_details['cover_image'] = None

            if locations:

                profile_details['confirmed_locations'] = locations

                loc = locations[0]
                city = loc.get('city')
                state = loc.get('geographicArea')
                country = loc.get('country')
                zipcode = loc.get('postalCode')
                addline1 = loc.get('line1')
                addline2 = loc.get('line2')

                if city:
                    profile_details['city'] = city

                if state:
                    profile_details['state'] = state

                if country:
                    profile_details['country'] = country

                if zipcode:
                    profile_details['zipcode'] = zipcode

                if addline1:
                    profile_details['addline1'] = addline1

                if addline2:
                    profile_details['addline2'] = addline2

            if self_declared_employees:
                profile_details['number_of_self_declared_employees'] = self_declared_employees

            if market and len(market) > 1:
                raw_text = market[1].get('localizedName')
                if raw_text:
                    profile_details['market'] = raw_text

            if tags:
                profile_details['tags'] = tags

            yield profile_details

    def follower_count(self, profile_detail):
        total_count = []
        for detail in profile_detail:
            count = detail.get('followerCount')
            if count:
                total_count.append(count)
        return total_count

    def raw_details(self, profile_detail):
        raw_details = []
        for detail in profile_detail:
            if len(detail) > 20:
                raw_details.append(detail)
        return raw_details
