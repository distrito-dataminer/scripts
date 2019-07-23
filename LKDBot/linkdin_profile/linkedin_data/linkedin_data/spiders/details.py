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
                'bcookie': 'v=2&efa04615-f7bd-4354-8059-dfd6ed04652c',
                'bscookie': 'v=1&20181126132739da50067d-d328-4290-8041-abc247df16e2AQGwX8Q57D6Zj8vKyMBnhxn1_I2JOw2S',
                'JSESSIONID': 'ajax:9028902051245035064',
                'visit': 'v=1&G',
                '_lipt': 'CwEAAAFsAF4cNzfXz9_l0j7z23C3gp_agTHV6aYJYn4zHO-i4WA8RrenV3bNJqjIZViX-nA1Tlt_nIhlTUR6kpngAavgtJtJbPwu2AjtpisDenD51Si6h8ZNtyKFr_R0F41nadH-QdRKNjuJr4u1ki0vSD3QTzglOIR0WxLKJYSkWfbrYvTxJKRFXU0izScRYIbfRy8g3B42PDvU9HxXv7DrtWOnIAbcZGTVnH3GOez4K5ci3h7-3Lq-ugTJpzP9FQ1V_sZp1OHJqwiShJf-5MEKl8Gq9Xy_zD9_hYiDvmNVPOV2Gq83IVwrJBJm3M9twXoMx19vyXp6Bg3UEM18UjPZyd0odsNLM9mxYnEYwGeY4ift7oEwmd5TmcqFLF8',
                'org_tcphc': 'true',
                'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-1303530583%7CMCIDTS%7C18095%7CMCMID%7C91815213977225861640575468564591355059%7CMCOPTOUT-1563400605s%7CNONE%7CvVersion%7C3.3.0',
                'UserMatchHistory': 'AQJmMWMvLsah-QAAAWwB_I_CBMAviMvfvjwVouA9rW98tzCKjVFsQLdkdgp811R4Q_MYbgH9mzuqOpw54IPBtHFNXkelKxSFkxuEdQxhCdKqONXgKkyHxla8g2quWslx0bqn0Tx7hcueWqHiV3rbwLBOTt3CQOI7mSal29FL0Ba3TSgH',
                'VID': 'V_2019_03_14_16_1004509',
                'utag_main': 'v_id:016a03d88eb7000f0d6316193d310004e00fe00d00bd0$_sn:3$_se:3$_ss:0$_st:1562880149903$vapi_domain:linkedin.com$ses_id:1562878260064%3Bexp-session$_pn:3%3Bexp-session',
                'sl': 'v=1&yXMhj',
                'liap': 'true',
                'li_at': 'AQEDARvom5kDY1-sAAABa1JFHJ0AAAFsGrU3pE4ACHGxnxB0A7JSCstXcJDRQ82dEiMtoImToQ6XGQ7B6-kpe3hxjwf6e3SPZ13-bA9y6CijG8ow7PSFxaQ1zQSdeAGouV6tlWvRh3G8HWftplGItHCl',
                'lang': 'v=2&lang=pt-br',
                'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
                'sdsc': '22%3A1%2C1563283046933%7ECONN%2C0DlDm398hxmixclt%2FrV%2BAIoixHy0%3D',
                'PLAY_SESSION': '29e0131d737670cfa65319d3c1d6e6c515567710-chsInfo=27bf9159-0ff1-423d-9b61-e0f8f93fc97f+premium_inmail_profile_upsell',
                'lidc': 'b=TB17:g=2728:u=175:i=1563401421:t=1563487803:s=AQHK3B6oiPcZAaKnJKG5J6wq8a6fvOZ_',
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
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
