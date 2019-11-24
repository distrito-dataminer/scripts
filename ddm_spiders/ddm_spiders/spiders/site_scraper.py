# -*- coding: utf-8 -*-
import scrapy
from collections import OrderedDict
import re
from unidecode import unidecode
from more_itertools import unique_everseen as unique
from urllib.parse import urlparse
import csv
import os
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'If-Modified-Since': 'Tue, 20 Aug 2019 17:17:02 GMT',
    'If-None-Match': 'W/5d5c2b0e-1c27',
    'Cache-Control': 'max-age=0',
}

terms_terms = ['terms', 'termos', 'condicoes', 'conditions']
privacy_terms = ['privacidade', 'privacy', 'política', 'policy']
contact_terms = ['contact', 'contato', 'fale', 'conosco', 'talk']
cnpj_regex = re.compile(r'\d{2}\.?\d{3}\.?\d{3}\/\d{4}-\d{2}', re.IGNORECASE)
linkedin_regex = re.compile(
    r'linkedin\.com\/(company|showcase|school)\/[^\/?"]*', re.IGNORECASE)
facebook_regex = re.compile(
    r'facebook\.com\/(pg\/|page\/|pages\/)?[^\/&?\s"]*', re.IGNORECASE)
twitter_regex = re.compile(r'twitter\.com\/[^\/&?"]*', re.IGNORECASE)
instagram_regex = re.compile(r'instagram\.com\/[^&?\/"]*', re.IGNORECASE)
crunchbase_regex = re.compile(
    r'crunchbase\.com\/organization\/[^"&?\/]*', re.IGNORECASE)
email_regex = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-z]+)")

invalid_emails = ['@sentry', '@example', '@exemplo', '@sentry.io', 'communities-translations',
                  'ajax-loader', 'communities-blog-viewer-app', 'suporte@contabilizei.com.br']


class SiteSpider(scrapy.Spider):

    name = 'sitescraper'

    startup_list = []

    if 'sitedata.csv' in os.listdir('C:\\Test\\'):
        with open('C:\\Test\\sitedata.csv', 'r', encoding='utf8') as f:
            startup_csv = csv.DictReader(f)
            for startup in startup_csv:
                startup_list.append(startup)
            f.close()

    #startup_list = [startup for startup in startup_list if 'Tirar?' not in startup or startup['Tirar?'] == '']
    urls = [startup['Site'] for startup in startup_list if startup['Site']]
    allowed_domains = [domain.replace(
        'http://', '').replace('https://', '') for domain in urls]
    handle_httpstatus_list = [i for i in range(399, 1000)]

    def start_requests(self):

        for url in self.urls:
            yield(scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'original_url': url}, errback=self.error_parse))

    def parse(self, response):

        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        now_ns = datetime.now().timestamp()

        site_info = OrderedDict()
        site_info['timestamp'] = now
        site_info['timestamp_ns'] = now_ns
        site_info['base_url'] = response.request.meta['original_url']
        site_info['url'] = response.request.url
        site_info['final_url'] = response.url
        site_info['domain'] = urlparse(
            response.url).scheme+'://'+urlparse(response.url).netloc+'/'
        site_info['response'] = response.status
        site_info['depth'] = response.meta['depth']

        if response.status != 200:
            yield site_info

        cnpj_list = []
        facebook_list = []
        linkedin_list = []
        twitter_list = []
        instagram_list = []
        crunchbase_list = []
        email_list = []

        html_text = response.text
        mo = re.findall(cnpj_regex, html_text)
        if mo:
            for cnpj in mo:
                cnpj_list.append(cnpj)
            cnpj_list = list(unique(cnpj_list))
            while '00.000.000/0000-00' in cnpj_list:
                cnpj_list.remove('00.000.000/0000-00')
            site_info['cnpj_all'] = ','.join(cnpj_list)
            for i, cnpj in enumerate(cnpj_list):
                site_info['cnpj_{}'.format(i+1)] = cnpj

        site_links = response.xpath('//a')
        for link in site_links:

            link_text = ''.join(link.xpath('.//text()').extract())
            link_url = str(
                urlparse(link.xpath('./@href').extract_first()).geturl()).lower()

            if '.pdf' in link_url:
                continue

            fb_search = re.search(facebook_regex, link_url)
            lkd_search = re.search(linkedin_regex, link_url)
            tt_search = re.search(twitter_regex, link_url)
            ig_search = re.search(instagram_regex, link_url)
            cb_search = re.search(crunchbase_regex, link_url)

            if fb_search:
                facebook_list.append(fb_search.group())
                continue
            if lkd_search:
                linkedin_list.append(lkd_search.group())
                continue
            if tt_search:
                twitter_list.append(tt_search.group())
                continue
            if ig_search:
                instagram_list.append(ig_search.group())
                continue
            if cb_search:
                crunchbase_list.append(cb_search.group())
                continue
            if 'mailto:' in link_url:
                email_list.append(link_url.replace(
                    'mailto:', '').split('?')[0].strip())
                continue
            if 'email:' in link_url:
                email_list.append(link_url.replace(
                    'email:', '').split('?')[0].strip())
                continue

            for term in terms_terms:
                if term in unidecode(link_text.lower()):
                    yield response.follow(url=link_url, meta={'original_url': response.request.meta['original_url']})

            for term in privacy_terms:
                if term in unidecode(link_text.lower()):
                    yield response.follow(url=link_url, meta={'original_url': response.request.meta['original_url']})

            for term in contact_terms:
                if term in unidecode(link_text.lower()):
                    yield response.follow(url=link_url, meta={'original_url': response.request.meta['original_url']})

        site_text = response.xpath('//text()').extract()
        for text in site_text:
            if type(text) == str:
                email_search = re.search(email_regex, text)
                if email_search:
                    email_list.append(email_search.group())
            if type(text) == list:
                for corpus in text:
                    email_search = re.search(email_regex, corpus)
                    if email_search:
                        email_list.append(email_search.group())

        facebook_list = sorted(list(unique(facebook_list)))
        linkedin_list = sorted(list(unique(linkedin_list)))
        twitter_list = sorted(list(unique(twitter_list)))
        instagram_list = sorted(list(unique(instagram_list)))
        email_list = sorted(list(unique(email_list)))

        for email in email_list:
            for invalid_email in invalid_emails:
                if invalid_email in email and email in email_list:
                    email_list.remove(email)

        site_info['facebook_all'] = ','.join(facebook_list)
        site_info['linkedin_all'] = ','.join(linkedin_list)
        site_info['twitter_all'] = ','.join(twitter_list)
        site_info['instagram_all'] = ','.join(instagram_list)
        site_info['email_all'] = ','.join(email_list)

        for i, facebook in enumerate(facebook_list):
            site_info['facebook_{}'.format(i+1)] = 'http://'+facebook
        for i, linkedin in enumerate(linkedin_list):
            site_info['linkedin_{}'.format(i+1)] = 'http://'+linkedin
        for i, twitter in enumerate(twitter_list):
            site_info['twitter_{}'.format(i+1)] = 'http://'+twitter
        for i, instagram in enumerate(instagram_list):
            site_info['instagram{}'.format(i+1)] = 'http://'+instagram
        for i, email in enumerate(email_list):
            site_info['email_{}'.format(i+1)] = email

        yield site_info

    def error_parse(self, failure):

        original_url = failure.request.meta['original_url']

        if 'www' not in failure.request.url:
            new_url = failure.request.url.replace('http://', 'http://www.')
            yield scrapy.Request(url=new_url, headers=headers, callback=self.parse, meta={'original_url': original_url}, errback=self.error_parse)
        elif 'https' not in failure.request.url:
            new_url = failure.request.url.replace('http://', 'https://')
            yield scrapy.Request(url=new_url, headers=headers, callback=self.parse, meta={'original_url': original_url}, errback=self.error_parse)

        else:
            site_info = OrderedDict()
            site_info['base_url'] = original_url
            site_info['url'] = failure.request.url
            site_info['response'] = repr(failure)
            yield(site_info)
