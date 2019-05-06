# -*- coding: utf-8 -*-

import json
import requests
import csv
import scrapy

from scrapy import Selector
from urllib.parse import urljoin


class LinkedinData(scrapy.Spider):
    name = "link_din_crawler"
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

            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'TE': 'Trailers',
                }
            
            cookies = {
                    'bcookie': 'v=2&efa04615-f7bd-4354-8059-dfd6ed04652c',
                    'bscookie': 'v=1&20181126132739da50067d-d328-4290-8041-abc247df16e2AQGwX8Q57D6Zj8vKyMBnhxn1_I2JOw2S',
                    'JSESSIONID': 'ajax:9028902051245035064',
                    'visit': 'v=1&G',
                    '_lipt': 'CwEAAAFqftIBN7vh3Ac3bEtTZXhdii-yODWsk7QHtmt9VKuKUn5VG561yhPza-t7aX0L2d-b3z07Lqv8ciDsp5JxqilHQKzjVXnUNeDSt6OcsSUeJYWDD86TsmHW2LeiT4E3avoquQ16bgFzCRNZe1kxMEvbli1Z6glGdpCrzG4Zj1bqYF2w0PRacgM-0WgJANPvDjPsIvGuP3Fs7g4XB9hJ8o-dJwJVcPajtAer12H9DHFM9onxCREkksXeosI34lvif8wsNFE_TozrGK8zRx0bzmpd7YK4TqYX50QX_oK7fAiI04MborcKh_Wm7lCatcdrhRNvU6B98Zt03E59uqjOWDKcEfhiv_2yg69oOliN9nc',
                    'org_tcphc': 'true',
                    'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-1303530583%7CMCIDTS%7C18019%7CMCMID%7C91815213977225861640575468564591355059%7CMCOPTOUT-1556924390s%7CNONE%7CvVersion%7C3.3.0',
                    'UserMatchHistory': 'AQLSsBUpfxHX0gAAAWp_fwNu3TvdVh3vch3dQLzgu6fYmHpKiqyXBKBfsNlnjCzw9vekN_ldEBEoxo8uuaTwmlF5FVkwZwKuScTFaUkmOpdxGMcY3Av6pcgnKHnHoGhX6GzoizM7ORSVLlI',
                    'VID': 'V_2019_03_14_16_1004509',
                    'utag_main': 'v_id:016a03d88eb7000f0d6316193d310004e00fe00d00bd0$_sn:2$_se:1$_ss:1$_st:1554846526748$vapi_domain:linkedin.com$ses_id:1554844726748%3Bexp-session$_pn:1%3Bexp-session',
                    'fid': 'AQFNhFFcFczmzQAAAWp-8h9vBBICARNDF9u6zrFVkEM3z3swMDDtkLYeOu9SOxNWXmD8qSiJY0VDZA',
                    'sl': 'v=1&X4pb2',
                    'PLAY_SESSION': '5a5da1cee44d0f9ff25e0ea14fe0fa28d594065e-chsInfo=120c1a81-a476-4bed-97ed-3d89ddbdd742+premium_inmail_profile_upsell',
                    'sdsc': '1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D',
                    'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
                    'SID': '68f7d811-0ee9-4d4d-82a4-f86265e15804',
                    'lidc': 'b=VB17:g=2451:u=96:i=1556907980:t=1556991990:s=AQFFt5NcXJPO2ONylBEBfrg69DKEPn3f',
                    'li_at': 'AQEDARvom5kBZXlpAAABan7yddEAAAFqov750U0AmIWKnavjPCf5RyrVaUmcYR-dNXzgyz59AE3CksfhbFHDQF7HdVXa_H5WlatQLLbN_FCkgIcleZP7VXqvpjXmCKqSaeBuyS_X2omvK9gyGKznKTiS',
                    'liap': 'true',
                    'lang': 'v=2&lang=pt-br',
                }

            raw_text = requests.get(url, headers=headers, cookies=cookies)

            response = raw_text.content
            html_response = Selector(text=response)

            raw_details = html_response.xpath('//*[contains(text(),"backgroundCoverImage")]/text()').extract_first()

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
                        profile_details['cover_image'] = raw_image[0].get('fileIdentifyingUrlPathSegment')
            else:
                profile_details['cover_image'] = None

            if locations:
                loc = locations[0]
                city = loc.get('city')
                state = loc.get('geographicArea')
                country = loc.get('country')

                if city:
                    profile_details['city'] = city

                if state:
                    profile_details['state'] = state

                if country:
                    profile_details['country'] = country

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
