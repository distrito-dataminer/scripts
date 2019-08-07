# -*- coding: utf-8 -*-

import json
import requests
import csv
import scrapy
import re

from scrapy import Selector
from urllib.parse import urljoin

cookies = {
    'mcd': '3',
    'csrftoken': 'MTWskBWjUd2LyEjYKaU7qm5PyKDImg3l',
    'mid': 'XAbUTQALAAHKOqsj5v_3Py1prmLV',
    'fbm_124024574287414': 'base_domain=.instagram.com',
    'ds_user_id': '3168633691',
    'sessionid': '3168633691%3AyOMPnsQtQqk0zY%3A16',
    'shbid': '17121',
    'shbts': '1565023335.8186018',
    'rur': 'PRN',
    'urlgen': '{\\"179.191.65.154\\\\:',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
}

class LinkedinData(scrapy.Spider):
    name = "lkdcrawler"
    start_urls = ['https://www.linkedin.com/']
    allowed_domains = ["www.linkedin.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }

    def parse(self, response):
        profiles = []
        f = open(r'C:\test\lkddata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['LinkedIn']
            if 'linkedin.com/' in url:
                profiles.append(url)
        for profile in profiles:

            url = urljoin(self.start_urls[0], profile.split('.com/')[1])

            response = requests.get(url, headers=headers, cookies=cookies)

            raw_text = response.content
            html_response = Selector(text=raw_text)

            raw_details = html_response.xpath(
                '//*[contains(text(),"backgroundCoverImage")]/text()').extract_first()

            if not raw_details:
                continue

            if 'fs_normalized_company:' in raw_details:
                companyIdRegex = re.compile(r'fs_followingInfo:urn:li:company:(\d+)')
                companyId = re.findall(companyIdRegex, raw_details)[0]

            details = json.loads(raw_details)
            profile_details = {}

            profile_detail = details['included']
            details_text = self.raw_details(profile_detail)

            if not details_text:
                continue

            detail = details_text[0]

            if companyId:
                count = self.follower_count_withId(profile_detail, companyId)
            else:
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
                profile_details['follower_count'] = count

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
        count = ''
        for detail in profile_detail:
            if 'entityUrn' in detail:
                if 'fs_followingInfo:urn:li:company' in detail['entityUrn']:
                    count = detail.get('followerCount')
        return count
    
    def follower_count_withId(self, profile_detail, companyId):
        count = ''
        for detail in profile_detail:
            if 'entityUrn' in detail:
                if 'fs_followingInfo:urn:li:company:'+str(companyId) in detail['entityUrn']:
                    count = detail.get('followerCount')
        return count

    def raw_details(self, profile_detail):
        raw_details = []
        for detail in profile_detail:
            if len(detail) > 20:
                raw_details.append(detail)
        return raw_details

class LinkedinProfileData(scrapy.Spider):
    name = "lkdprofilecrawler"
    start_urls = ['https://www.linkedin.com/']
    allowed_domains = ["www.linkedin.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }

    def parse(self, response):
        profiles = []
        f = open(r'C:\test\lkdprofiledata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['LinkedIn']
            if 'linkedin.com/' in url:
                profiles.append(url)
        for profile in profiles:

            url = urljoin(self.start_urls[0], profile.split('.com/')[1])

            response = requests.get(url, headers=headers, cookies=cookies)

            raw_text = response.content
            html_response = Selector(text=raw_text)

            raw_personal_details = html_response.xpath(
                '//*[contains(text(),"summary")]/text()').extract_first()
            raw_social_details = html_response.xpath(
                '//*[contains(text(),"followersCount")]/text()').extract_first()

            if not raw_personal_details:
                continue

            profile_details = {}
            personal_details = json.loads(raw_personal_details)

            if personal_details:
                
                profile_info = personal_details.get('included')

                if profile_info:

                    for item in profile_info:
                        if 'summary' in item:
                            profile_basicinfo = item

                    if profile_basicinfo:
                            
                        firstName = profile_basicinfo.get('firstName')
                        lastName = profile_basicinfo.get('lastName')
                        summary = profile_basicinfo.get('summary')
                        headline = profile_basicinfo.get('headline')
                        industryName = profile_basicinfo.get('industryName')
                        locationName = profile_basicinfo.get('locationName')
                        address = profile_basicinfo.get('address')
                        geoCountryName = profile_basicinfo.get('geoCountryName')

                        if url:
                            profile_details['url'] = url.replace('https://www.', 'http://')

                        if firstName:
                            profile_details['first_name'] = firstName

                        if lastName:
                            profile_details['last_name'] = lastName
                        
                        if summary:
                            profile_details['summary'] = summary
                        
                        if headline:
                            profile_details['headline'] = headline

                        if industryName:
                            profile_details['industry_name'] = industryName

                        if locationName:
                            profile_details['location_name'] = locationName

                        if address:
                            profile_details['address'] = address

                        if geoCountryName:
                            profile_details['country_name'] = geoCountryName

            if raw_social_details:
                social_details = json.loads(raw_social_details)

                if social_details:
                    social_details_full = social_details.get('data')

                    if social_details_full:
                        followers = social_details_full.get('followersCount')
                        connections = social_details_full.get('connectionsCount')

                    if followers:
                        profile_details['followers'] = followers

                    if connections:
                        profile_details['connections'] = connections

            yield profile_details

class FacebookData(scrapy.Spider):
    name = "fbcrawler"
    start_urls = ['https://www.facebook.com/']
    allowed_domains = ["www.facebook.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }
    headers['Accept-Language'] = 'en-US;q=0.5,en;q=0.3'

    def parse(self, response):
        
        profiles = []        
        likeRegex = re.compile(r'([\d,]+) people like this')
        followRegex = re.compile(r'([\d,]+) people follow this')

        f = open(r'C:\test\fbdata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['Facebook']
            if 'facebook.com/' in url:
                profiles.append(url)

        for profile in profiles:
            url = urljoin(self.start_urls[0], profile.split('.com/')[1])

            response = requests.get(url, headers=headers, cookies=cookies)

            raw_text = response.text

            likeMatch = re.search(likeRegex, raw_text)
            followMatch = re.search(followRegex, raw_text)

            profile_details = {}

            if likeMatch:
                likes = likeMatch.group(1)
                if likes:
                    profile_details['likes'] = likes.replace(',', '')

            if followMatch:
                follows = followMatch.group(1)
                if follows:
                    profile_details['follows'] = follows.replace(',', '')

            if url:
                profile_details['url'] = url.replace('https://www.', 'http://')

            yield profile_details

class TwitterData(scrapy.Spider):
    name = "ttcrawler"
    start_urls = ['https://www.twitter.com/']
    allowed_domains = ["www.twitter.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }
    headers['Accept-Language'] = 'en-US;q=0.5,en;q=0.3'

    def parse(self, response):
        
        profiles = []        

        f = open(r'C:\test\ttdata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['Twitter']
            if 'twitter.com/' in url:
                profiles.append(url)

        for profile in profiles:
            url = urljoin(self.start_urls[0], profile.split('.com/')[1])

            response = requests.get(url, headers=headers, cookies=cookies)

            raw_text = response.content

            html_response = Selector(text=raw_text)

            raw_info = html_response.xpath('//input[@class = "json-data"]/@value').extract_first()

            if not raw_info:
                continue
            
            full_info = json.loads(raw_info)
            
            info = full_info.get('profile_user')

            if not info:
                continue

            profile_details = {}

            profile_details['twitter_url'] = url.replace('https://www.', 'http://')

            for key in info:
                profile_details[key] = info[key]

            yield profile_details

class SimilarWebData(scrapy.Spider):
    name = "swcrawler"
    start_urls = ['https://www.similarweb.com/pt/website/']
    allowed_domains = ["www.similarweb.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }

    def parse(self, response):
        
        profiles = []        

        f = open(r'C:\test\swdata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['Site']
            if url:
                profiles.append(url)

        for profile in profiles:
            url = 'https://www.similarweb.com/pt/website/contabilizei.com.br'

            response = requests.get(url, headers=headers, cookies=cookies)
            print(response)

            raw_text = response.content

            html_response = Selector(text=raw_text)

            swInfo = html_response.xpath('//*[@class = "engagementInfo-valueNumber js-countValue"]/text()').extract()

            if not swInfo:
                continue
            
            profile_details = {}

            profile_details['url'] = url
            profile_details['Site'] = profile

            if len(swInfo) == 4:
                profile_details['totalVisits'] = swInfo[0]
                profile_details['timeSpent'] = swInfo[1]
                profile_details['pagesPerVisit'] = swInfo[2]
                profile_details['bounceRate'] = swInfo[3]

            yield profile_details

class LoveMondaysData(scrapy.Spider):
    name = "lmcrawler"
    start_urls = ['https://www.lovemondays.com.br/']
    allowed_domains = ["www.lovemondays.com.br"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }

    def parse(self, response):
        
        profiles = []        

        f = open(r'C:\test\lmdata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['LoveMondays']
            if url:
                profiles.append(url)

        for profile in profiles:
            url = urljoin(self.start_urls[0], profile.split('.com.br/')[1])

            response = requests.get(url, headers=headers, cookies=cookies)

            if response.status_code != 200:
                continue

            raw_text = response.content

            mo = re.search('{"overallRating".+"EmployerRatings"}', response.text)

            html_response = Selector(text=raw_text)

            avaliacoes = html_response.xpath('//*[@data-label = "Avaliações"]//span [@class = "num h2"]/text()').extract_first()
            salarios = html_response.xpath('//*[@data-label = "Salários"]//span [@class = "num h2"]/text()').extract_first()
            vagas = html_response.xpath('//*[@data-label = "Vagas"]//span [@class = "num h2"]/text()').extract_first()
            entrevistas = html_response.xpath('//*[@data-label = "Entrevistas"]//span [@class = "num h2"]/text()').extract_first()
            beneficios = html_response.xpath('//*[@data-label = "Benefícios"]//span [@class = "num h2"]/text()').extract_first()
            
            profile_details = {}

            profile_details['LoveMondays'] = url
            profile_details['Avaliações'] = avaliacoes
            profile_details['Salários'] = salarios
            profile_details['Vagas'] = vagas
            profile_details['Entrevistas'] = entrevistas
            profile_details['Benefícios'] = beneficios

            if mo:
                exceptions = ['__typename', 'ratedCeo']
                ratings = json.loads(mo.group())
                for key in ratings:
                    if key not in exceptions:
                        profile_details[key] = ratings[key]

            for key in profile_details:
                if profile_details[key]:
                    profile_details[key] = str(profile_details[key]).strip()

            yield profile_details

class InstagramData(scrapy.Spider):
    name = "igcrawler"
    start_urls = ['https://www.instagram.com/']
    allowed_domains = ["www.instagram.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }

    def parse(self, response):
        
        profiles = []        

        f = open(r'C:\test\igdata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)
        for row in reader:
            url = row['Instagram']
            if url:
                profiles.append(url)

        for profile in profiles:
            url = urljoin(self.start_urls[0], profile.split('.com/')[1])

            response = requests.get(url, headers=headers, cookies=cookies)

            raw_text = response.content

            html_response = Selector(text=raw_text)

            igInfo = html_response.xpath('//script[@type = "application/ld+json"]/text()').extract_first()
            igDesc = html_response.xpath('//meta [@property="og:description"]/@content').extract_first()

            if igInfo:
                igInfo = igInfo.strip()
                igInfo = json.loads(igInfo)
            else:
                continue
            
            profile_details = {}

            profile_details['instagram'] = profile
            profile_details['type'] = igInfo['@type']
            profile_details['name'] = igInfo['name']
            profile_details['alternate_name'] = igInfo['alternateName']
            profile_details['description'] = igInfo['description']
            profile_details['followers'] = igInfo['mainEntityofPage']['interactionStatistic']['userInteractionCount']
            profile_details['url'] = igInfo['url']
            profile_details['followers_desc'] = re.search(r'([\d\.,]+[^\d]+)(seguidores|followers)', igDesc, re.IGNORECASE).group(1).strip()
            profile_details['following_desc'] = re.search(r'([\d\.,]+[^\d]+)(seguindo|following)', igDesc, re.IGNORECASE).group(1).strip()
            profile_details['posts_desc'] = re.search(r'([\d\.,]+[^\d]+)(publicações|posts)', igDesc, re.IGNORECASE).group(1).strip()

            yield profile_details