#! python3
# sbConvert.py - Creates a list of startups from a StartupBase scraping result

import sys
import os
import re
import csv
import json

from utils import ddmdata, cleaner

startup_list = []
sb_path = 'C:\\Test\\SB\\'

file_list = os.listdir(sb_path)
json_list = []

if 'all_jsons.txt' in file_list:
    print('Using all_jsons.txt to speed up conversion.')
    with open(sb_path+'all_jsons.txt', 'r', encoding='utf8') as f:
        jsons_text = f.read()
        f.close()
    sb_jsons = jsons_text.split('\n---SEPARATOR---\n')
    sb_jsons = [x for x in sb_jsons if x]
    for sb_json in sb_jsons:
        sb_dict = json.loads(sb_json)
        json_list.append(sb_dict)
    print('Done.')

else:
    file_list = [item for item in file_list if '.json' in item]
    for sb_file in file_list:
        with open(sb_path+sb_file, encoding='utf8') as f:
            print('Converting JSON for {}'.format(sb_file))
            sb_json = f.read()
            sb_dict = json.loads(sb_json)
            json_list.append(sb_dict)
            f.close()

startup_list = [item for item in json_list if item and type(item) == dict]
team_list = [item for item in json_list if item and type(item) == list]

people_list = []
address_list = []

for startup in startup_list:

    if startup['slug']:
        startup['sb_url'] = 'http://startupbase.com.br/c/startup/{}'.format(
            startup['slug'])

    elif 'founded_at' in startup and startup['founded_at']:
        day, month, year = startup['founded_at'].split('/')
        startup['founded_date'] = '{}-{}-{}'.format(year, month, day)

    if 'links' in startup and startup['links']:
        for key in startup['links']:
            startup[key] = startup['links'].get(key)

    if 'segment' in startup and startup['segment']:
        startup['Setor SB'] = startup['segment'].get('primary')
    startup_badges = [badge.get('badge').get('name') for badge in startup.get('badges')]
    startup['Badges'] = ','.join(startup_badges)

    if 'startup' in startup and startup['startup']:
        info = startup.get('startup')
        startup['annual_revenue'] = info.get('annual_revenue')
        startup['employees'] = info.get('employees')
        startup['has_funding'] = startup.get('has_funding')
        if info.get('model'):
            startup['business_model'] = info.get('model').get('name')
        if info.get('phase'):
            startup['business_phase'] = info.get('phase').get('name')
        if info.get('target'):
            startup['business_target'] = info.get('target').get('name')

    if startup['adresses']:
        for address in startup['adresses']:
            end = {}
            for key in address:
                if key != 'city':
                    end[key] = address[key]
            if 'city' in address and address['city']:
                end['city'] = address['city'].get('name')
            if 'state' in address and address['state']:
                end['state'] = address['state'].get('uf')
                if address['is_parent'] == 1:
                    startup['Cidade'] = end['city']
                    startup['Estado'] = end['state']
            address_list.append(end)


for team in team_list:
    for member in team:
        person = {}
        for key in member:
            if key != 'user':
                person[key] = member[key]
        if 'user' in member and member['user']:
            user_info = member.get('user')
            for key in user_info:
                if key != 'links':
                    person[key] = user_info[key]
            if 'links' in user_info and user_info['links']:
                user_links = user_info['links']
                for key in user_links:
                    person[key] = user_links[key]
        people_list.append(person)


ddmdata.writecsv(startup_list, 'sb_startups.csv')
ddmdata.writecsv(address_list, 'sb_addresses.csv')
ddmdata.writecsv(people_list, 'sb_people.csv')

converted_startups = []
conversion_dict = {
    'name': 'Startup',
    'id_organization': 'ID StartupBase',
    'cnpj': 'CNPJ',
    'email': 'E-mail',
    'phone': 'Telefone',
    'short_description': 'Descrição curta',
    'description': 'Descrição',
    'tags': 'Tags',
    'profile_image': 'Logo SB',
    'is_active': 'Atividade SB',
    'is_verified': 'Verificada SB',
    'sb_url': 'StartupBase',
    'annual_revenue': 'Faturamento declarado',
    'employees': 'Faixa # de funcionários',
    'business_phase': 'Estágio da operação',
    'business_target': 'Público',
    'business_model': 'Modelo de negócio',
    'facebook': 'Facebook',
    'website': 'Site',
    'instagram': 'Instagram',
    'linkedin': 'LinkedIn',
    'medium': 'Medium',
    'twitter': 'Twitter',
    'googleplay': 'App (Play Store)',
    'youtube': 'YouTube',
    'appstore': 'App (App Store)'
}

same_name = ['Setor SB', 'Badges', 'Cidade', 'Estado']

for startup in startup_list:
    new_startup = {}
    for key, value in conversion_dict.items():
        if key in startup:
            new_startup[value] = startup[key]
    for key in same_name:
        if key in startup:
            new_startup[key] = startup[key]
    if 'founded_date' in startup and startup['founded_date']:
        year, month, day = startup['founded_date'].split('-')
        new_startup['Ano de fundação'] = year
    converted_startups.append(new_startup)

ddmdata.writecsv(converted_startups, 'sb_startups_converted.csv')
