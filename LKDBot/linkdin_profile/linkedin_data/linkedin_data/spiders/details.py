# -*- coding: utf-8 -*-

import json
import requests
import csv
import scrapy
import re
import bs4

from collections import OrderedDict
from more_itertools import unique_everseen as unique

from scrapy import Selector
from urllib.parse import urljoin

import urllib3
urllib3.disable_warnings()

cookies = {
    'bcookie': 'v=2&efa04615-f7bd-4354-8059-dfd6ed04652c',
    'bscookie': 'v=1&20181126132739da50067d-d328-4290-8041-abc247df16e2AQGwX8Q57D6Zj8vKyMBnhxn1_I2JOw2S',
    'JSESSIONID': 'ajax:9028902051245035064',
    'visit': 'v=1&G',
    '_lipt': 'CwEAAAFscov9DQg4viDZPquCLvPFbxTetUZ9_vwqRpula8nkJIIuyrAjhUHS-MyTTpB0iyT19N9Qey1asHpfuD1s14TvkQuYy5DT5oHXX4EwgN8ey07FzKm65Lj8p9RNchdI1t39vwnN1vk9pVyw72q3f9sLR66a4hvnC6h0_JVdyxM8DTLuNWaruigYEc8SDiuEDO6WXHUcrM4z1OguPeqvMv7Si9IlAYzSS5-ZQQTDHCDeWtR9esg7Foifwu4m7KoUNJUkPfETNxXJ4JuTA9fn4PU9tUSz7jcX49UTfiMc0_H31j0TLGHTesEcMHHBQj_T29OFCEm3rFl7CKKpwU1JFB6EGgTjwLuwQV4dWq7Ci0pEjQRZ6ZfjYA',
    'org_tcphc': 'true',
    'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-1303530583%7CMCIDTS%7C18117%7CMCMID%7C91815213977225861640575468564591355059%7CMCOPTOUT-1565379818s%7CNONE%7CvVersion%7C3.3.0',
    'UserMatchHistory': 'AQIGXrHHcZEoLQAAAWx3epJES9dlfAxOBwp_lm1xQ1Z0EQArLlvK7HWJgp6GBMSciRux5ykwO3hRUq5fbfH5HEiUK_AdDbSTSFdlHb0ux5X5zFSbhTBVfej_XpHGVn4szcp7pbgHSTlk0wj14oBZWqhx15CqVhnR4eww1GA0wg7hqhf6',
    'VID': 'V_2019_03_14_16_1004509',
    'utag_main': 'v_id:016a03d88eb7000f0d6316193d310004e00fe00d00bd0$_sn:3$_se:3$_ss:0$_st:1562880149903$vapi_domain:linkedin.com$ses_id:1562878260064%3Bexp-session$_pn:3%3Bexp-session',
    'sl': 'v=1&Vu5lY',
    'lissc1': '1',
    'lissc2': '1',
    'li_at': 'AQEDARvom5kCaTcCAAABbEMbkMQAAAFsjB2wy04AHQ_14jdHpTLSW4RycLgZWmUIm7KIHs59auV-TFq88Ll0Lw_fBjejleRp3sGftr8WJJxv35Rklc5uB0Qkz_GtPooTsfKwC9uoX-avLEirf_v6jknw',
    'liap': 'true',
    'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
    'sdsc': '22%3A1%2C1564769093865%7ECONN%2C0pTMJNBGrXfe7jSER3T96u%2Fb47f8%3D',
    'PLAY_SESSION': 'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiI2NTFjMjIxMy00M2RjLTQ0ODctOTRjMy0yOTc2MGUwOWE1NDB8MTU2NTI5MDU1OSIsInJlY2VudGx5LXNlYXJjaGVkIjoiIiwicmVmZXJyYWwtdXJsIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJhaWQiOiIiLCJSTlQtaWQiOiJ8MCIsInJlY2VudGx5LXZpZXdlZCI6IjE2NDYiLCJDUFQtaWQiOiJOMk00WlRjM05tTXROemt4T1MwMFpUSTBMVGc1TUdZdE9XWXdaVFpqTURkbU1ETXciLCJleHBlcmllbmNlIjoiZW50aXR5IiwiaXNfbmF0aXZlIjoiZmFsc2UiLCJ3aGl0ZWxpc3QiOiJ7fSIsInRyayI6IiJ9LCJuYmYiOjE1NjUyOTA1NjYsImlhdCI6MTU2NTI5MDU2Nn0.mHoFfcNFq7QMhwxLLI3XyRvU8mJDzWF0jldxHwsRqL0',
    'lang': 'v=2&lang=pt-br',
    'PLAY_LANG': 'en',
    'lidc': 'b=VB17:g=2656:u=211:i=1565372613:t=1565457463:s=AQGZVg0wYoL0-u_DxnhP1uNyZTWp3W5z',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.linkedin.com/feed/',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
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

class SiteScraper(scrapy.Spider):
    name = "sitescraper"
    custom_settings = {
        'DOWNLOAD_DELAY': 15
    }
    start_urls = ['https://www.instagram.com/']
    allowed_domains = ["www.instagram.com"]

    def parse(self, response):

        profiles = []        

        f = open(r'C:\test\ssdata.csv', 'r', encoding='utf8')
        reader = csv.DictReader(f)

        for row in reader:
            url = row['Site']
            if url:
                profiles.append(url)
        
        for profile in profiles:
            
            startup = {}
            startup['Site'] = profile
            startup['E-mail'] = ''

            site, response = self.getSite(startup['Site'])
            startup['Response'] = response
            if response != 200:
                continue
            startup['CNPJ'] = self.getCnpj(site)
            startup['CNPJ'] = self.getRegistro(startup['Site'])
            startup['LinkedIn'] = self.getLinkedin(site)
            startup['Facebook'] = self.getFacebook(site)
            startup['Twitter'] = self.getTwitter(site)
            startup['Instagram'] = self.getInstagram(site)
            startup['Crunchbase'] = self.getCrunchbase(site)
            startup['E-mail'] = self.getEmail(site, startup['E-mail'])

            yield startup

    def getSite(self, site):
        if ("http" and "://") not in site:
            site = "http://" + site
        try:
            res = requests.get(site, verify=False, timeout=(2, 15), headers=headers)
        except Exception as e:
            try:
                print('Erro. Adicionando WWW.')
                site = site.replace('http://', 'http://www.')
                res = requests.get(site, verify=False, timeout=(2, 15))
            except:
                print('Erro mesmo com WWW. Enviando erro original.')
                return 'ERRO', repr(e)
        if res.status_code != 200:
            try:
                if 'http://www.' not in site:
                    print('Status code ruim. Adicionando WWW.')
                    site = site.replace('http://', 'http://www.')
                    res2 = requests.get(site, verify=False, timeout=(2, 15))
                    if res2.status_code == 200:
                        soup = bs4.BeautifulSoup(res2.text, features="lxml")
                        return soup, res2.status_code
                    else:
                        print('Adicionar o WWW não resolveu. Prosseguindo com status code original.')
            except:
                print('Erro ao adicionar WWW. Prosseguindo com status code ruim.')
        soup = bs4.BeautifulSoup(res.text, features="lxml")
        return soup, res.status_code

    # Busca números no formato de CNPJ no site e retorna os resultados
    def scrapeCnpj(self, content):
        cnpjRegex = re.compile(r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}")
        results = cnpjRegex.findall(content.text)
        for item in results:
            mo = cnpjRegex.search(item)
            item = mo.group()
        return results

    # Busca links na página contendo "termos" ou "terms" e retorna uma lista deles
    def getTermos(self, content):
        termosRegex = re.compile(".*(Termos|Terms).*", re.IGNORECASE)
        termosResults = content.find_all("a", href=True, title=termosRegex)
        results = []
        for item in termosResults:
            site, response = self.getSite(item['href'])
            if response != 200:
                continue
            result = self.scrapeCnpj(site)
            results += result
        return results

    # Busca links na página contendo "privacidade" ou "privacy" e retorna uma lista deles
    def getPrivacidade(self, content):
        privacidadeRegex = re.compile(".*(Privacidade|Privacy).*", re.IGNORECASE)
        privacidadeResults = content.find_all("a", href=True, title=privacidadeRegex)
        results = []
        for item in privacidadeResults:
            site, response = self.getSite(item['href'])
            if response != 200:
                continue
            result = self.scrapeCnpj(site)
            results += result
        return results
        
    # Roda o scrapeCnpj() no site principal, página de termos e página de política de privacidade, retorna lista com todos os resultados
    def getCnpj(self, content):
        result = []
        mainScrape = self.scrapeCnpj(content)
        termosScrape = self.getTermos(content)
        privacidadeScrape = self.getPrivacidade(content)
        result = mainScrape + termosScrape + privacidadeScrape
        result = list(OrderedDict.fromkeys(result))
        if result == []:
            print("Nenhum CNPJ encontrado.")
            return ''
        elif len(result) == 1:
            print("Um CNPJ encontrado: " + result[0])
            return result[0]
        elif len(result) > 1:
            print("Mais de um CNPJ encontrado: " + str(result))
            return ','.join(result)

    # TODO: buscar CNPJ no registro do site no registro.br
    def getRegistro(self, url):
        url = url.strip('/').replace('http://', '')
        if url[-3:] == ".br":
            print("CNPJ pode estar no registro do domínio! Verificar WHOIS.")
            return ""
        else:
            return ""

#    def getLogo(content):
#        logoRegex = re.compile(r"""(https?:\/\/.[^"\s]*?logo.[^"\s]*?\.(png|jpg|svg|tif|jpeg|bmp))""", re.IGNORECASE)
#        matches = re.findall(logoRegex, str(content))
#        results = []
#        for item in matches:
#            results.append(item[0])
#        if results == []:
#            result = ""
#            print("Nenhum Logo encontrado.")
#        elif len(results) == 1:
#            print("Um Logo encontrado: " + results[0])
#            result = results[0]
#        elif len(results) > 1:
#            print("Mais de um Logo encontrado: " + str(results))
#            result = results
#        return result

    # Busca links para páginas de empresa no LinkedIn e retorna os resultados
    def getLinkedin(self, content):
        lkdRegex = re.compile(r"linkedin\.com\/company\/[^&?\/]*", re.IGNORECASE)
        soupResults = content.find_all("a", href=lkdRegex)
        result = []
        for item in soupResults:
            mo = lkdRegex.search(item['href'])
            result.append("http://" + mo.group().split("?", 1)[0].split("&", 1)[0].replace('/about',"").strip('/').lower()) 
        result = list(OrderedDict.fromkeys(result))
        if result == []:
            result = ""
            print("Nenhum LinkedIn encontrado.")
        elif len(result) == 1:
            print("Um LinkedIn encontrado: " + result[0])
            result = result[0]
        elif len(result) > 1:
            print("Mais de um LinkedIn encontrado: " + str(result))
        return result

    # Busca links para o Facebook e retorna os resultados
    def getFacebook(self, content):
        fbRegex = re.compile(r"(facebook|fb)\.com\/(pg\/|page\/|pages\/)?[^\/?&\.]*", re.IGNORECASE)
        soupResults = content.find_all('a', href=fbRegex)
        result = []
        for item in soupResults:
            mo = fbRegex.search(item['href'])
            url = ("http://" + mo.group().replace('/pages','').replace('/pg', '').replace('/profile', '').replace('fb.com', 'facebook.com').strip('/').lower())
            if url != "http://facebook.com":
                result.append(url)
        result = list(OrderedDict.fromkeys(result))
        if result == []:
            result = ""
            print("Nenhum Facebook encontrado.")
        elif len(result) == 1:
            print("Um Facebook encontrado: " + result[0])
            result = result[0]
        elif len(result) > 1:
            print("Mais de um Facebook encontrado: " + str(result))
        return result

    # Busca links para o Instagram e retorna os resultados
    def getInstagram(self, content):
        igRegex = re.compile(r"instagram\.com\/[^&?\/]*", re.IGNORECASE)
        soupResults = content.find_all("a", href=igRegex)
        result = []
        for item in soupResults:
            mo = igRegex.search(item['href'])
            result.append("http://" + mo.group().replace('/about',"").strip('/').lower())
        result = list(OrderedDict.fromkeys(result))
        if result == []:
            result = ""
            print("Nenhum Instagram encontrado.")
        elif len(result) == 1:
            print("Um Instagram encontrado: " + result[0])
            result = result[0]
        elif len(result) > 1:
            print("Mais de um Instagram encontrado: " + str(result))
        return result

    # Busca links para o Twitter e retorna os resultados
    def getTwitter(self, content):
        ttRegex = re.compile(r"twitter\.com\/[^&?\/].*", re.IGNORECASE)
        soupResults = content.find_all("a", href=ttRegex)
        result = []
        for item in soupResults:
            mo = ttRegex.search(item['href'])
            result.append("http://" + mo.group().replace('/about',"").strip('/').lower())
        result = list(OrderedDict.fromkeys(result))
        if result == []:
            result = ""
            print("Nenhum Twitter encontrado.")
        elif len(result) == 1:
            print("Um Twitter encontrado: " + result[0])
            result = result[0]
        elif len(result) > 1:
            print("Mais de um Twitter encontrado: " + str(result))
        return result

    # Busca links para páginas de organização do Crunchbase e retorna os resultados
    def getCrunchbase(self, content):
        cbRegex = re.compile(r"crunchbase\.com\/organization\/[^&?\/]*", re.IGNORECASE)
        soupResults = content.find_all("a", href=cbRegex)
        result = []
        for item in soupResults:
            mo = cbRegex.search(item['href'])
            result.append("http://" + mo.group().split("?", 1)[0].split("&", 1)[0].strip('/').lower())
        result = list(OrderedDict.fromkeys(result))
        if result == []:
            result = ""
            print("Nenhum Crunchbase encontrado.")
        elif len(result) == 1:
            print("Um Crunchbase encontrado: " + result[0])
            result = result[0]
        elif len(result) > 1:
            print("Mais de um Crunchbase encontrado: " + str(result))
        return result

    def scrapeEmail(self, content):
        emailRegex = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
        results = emailRegex.findall(content.text)
        for item in results:
            mo = emailRegex.search(item)
            item = mo.group()
        return results

    def getContato(self, content):
        contatoRegex = re.compile(".*(Contato|Contact|Fale Conosco).*", re.IGNORECASE)
        termosResults = content.find_all("a", href=True, title=contatoRegex)
        results = []
        for item in termosResults:
            site, response = self.getSite(item['href'])
            if response != 200:
                continue
            result = self.scrapeEmail(site)
            results += result
        return results

    def getEmail(self, content, currentemails):
        result = []
        mainScrape = self.scrapeEmail(content)
        contatoScrape = self.getContato(content)
        result += mainScrape + contatoScrape
        result = list(unique(result))
        if result == []:
            print("Nenhum E-mail encontrado.")
        elif len(result) == 1:
            print("Um E-mail encontrado: " + result[0])
        elif len(result) > 1:
            print("Mais de um E-mail encontrado: " + str(result))
        if currentemails != '':
            currentemailslist = currentemails.split(',')
            result = result + currentemailslist
            result = list(unique(result))
        return ','.join(result)

