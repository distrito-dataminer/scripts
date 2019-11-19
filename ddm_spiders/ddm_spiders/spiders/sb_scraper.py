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
    'Upgrade-Insecure-Requests': '0',
    'If-Modified-Since': 'Tue, 20 Aug 2019 17:17:02 GMT',
    'If-None-Match': 'W/5d5c2b0e-1c27',
    'Cache-Control': 'max-age=0',
}

search_html = ''
if 'sbdata.html' in os.listdir('C:\\Test\\'):
    with open('C:\\Test\\sbdata.html', 'r', encoding='utf8') as f:
        search_html = f.read()
    f.close()

slug_regex = re.compile(r'/c/startup/([^"\s]+)')
slugs = re.findall(slug_regex, search_html)
already_scraped = [item.replace('.json', '') for item in os.listdir('C:\\Test\\SB\\')]
final_slugs = [slug for slug in slugs if slug not in already_scraped]
if len(slugs) != len(final_slugs):
    print('Out of {} startups, {} startups were already scraped and will not be redone.'.format(len(slugs), len(slugs) - len(final_slugs)))
base_url = 'https://api-leg.startupbase.com.br/startups/slug/'

class SBSpider(scrapy.Spider):

    name = 'sbscraper'

    startup_urls = [(base_url + slug) for slug in final_slugs]
    team_urls = [(base_url + slug + '/team') for slug in final_slugs]
    start_urls = sorted(startup_urls + team_urls)

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        'CONCURRENT_REQUESTS_PER_IP': 100,
        'ITEM_PIPELINES': {'ddm_spiders.pipelines.JsonWriterPipeline': 300}
    }

    def parse(self, response):

        slug = response.request.url.replace('.json', '').replace(base_url, '')
        
        if '/team' in slug:
            slug = slug.replace('/team', '')
            slug = slug + '_TEAM'

        result = {
            'name': slug,
            'content': response.text
        }

        yield result

class SBTeamSpider(scrapy.Spider):

    name = 'sbteamscraper'

    start_urls = [(base_url + slug + '/team') for slug in final_slugs]

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        'CONCURRENT_REQUESTS_PER_IP': 100,
        'ITEM_PIPELINES': {'ddm_spiders.pipelines.JsonWriterPipeline': 300}
    }

    def parse(self, response):

        slug = response.request.url.replace('.json', '').replace(base_url, '').replace('/team', '')

        
        result = {
            'name': slug+'_TEAM_DATA',
            'content': response.text
        }

        yield result