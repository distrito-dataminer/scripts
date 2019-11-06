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

for sb_file in os.listdir(sb_path):
    with open(sb_path+sb_file, encoding='utf8') as f:
        print('Converting JSON for {}'.format(sb_file))
        sb_json = f.read()
        sb_dict = json.loads(sb_json)
        if 'slug' not in sb_dict:
            print(
                'Possível erro com o arquivo {}. Pode causar problemas.'.format(sb_file))
        startup_list.append(sb_dict)
        f.close()

people_list = []
address_list = []

for startup in startup_list:
    if startup['slug']:
        startup['sb_url'] = 'http://startupbase.com.br/c/startup/{}'.format(
            startup['slug'])
    if startup['founded_date']:
        day, month, year = startup['founded_date'].split('/')
        startup['founded_date'] = '{}-{}-{}'.format(year, month, day)
    for link in startup['links']:
        if link['link_type'] == 1:
            startup['Site'] = link['url']
        if link['link_type'] == 2:
            startup['Facebook'] = link['url']
        if link['link_type'] == 3:
            startup['Twitter'] = link['url']
        if link['link_type'] == 4:
            startup['LinkedIn'] = link['url']
        if link['link_type'] == 5:
            startup['YouTube'] = link['url']
        if link['link_type'] == 6:
            startup['Instagram'] = link['url']
        if link['link_type'] == 7:
            startup['Medium'] = link['url']
        if link['link_type'] == 9:
            startup['App (App Store)'] = link['url']
        if link['link_type'] == 10:
            startup['App (Play Store)'] = link['url']
    for group in startup['groups']:
        startup['Setor SB'] = group['name']
    startup_badges = sorted([badge['name'] for badge in startup['badges']])
    startup['Badges'] = ','.join(startup_badges)
    if startup['startup']:
        startup['annual_revenue'] = startup['startup']['annual_revenue']
        startup['employees'] = startup['startup']['employees']
        startup['has_funding'] = startup['startup']['has_funding']
        if startup['startup']['model']:
            startup['business_model'] = startup['startup']['model']['name']
        if startup['startup']['phase']:
            startup['business_phase'] = startup['startup']['phase']['name']
        if startup['startup']['target']:
            startup['business_target'] = startup['startup']['target']['name']
    if startup['relations']:
        for relation in startup['relations']:
            person = {}
            person['organization'] = relation['fk_organization']
            person['member_id'] = relation['fk_member']
            person['is_founder'] = relation['is_founder']
            person['is_admin'] = relation['is_admin']
            person['is_aware'] = relation['is_aware']
            person['is_visible'] = relation['is_visible']
            if relation['role']:
                person['role'] = relation['role']['name']
            if relation['member']:
                member = relation['member']
                person['first_name'] = member['first_name']
                person['last_name'] = member['last_name']
                person['email'] = member['email']
                person['profile_image'] = member['profile_image']
            for link in member['links']:
                if link['link_type'] == 4:
                    person['linkedin'] = link['url']
            people_list.append(person)
    if startup['adresses']:
        for address in startup['adresses']:
            end = {}
            for key in address:
                if key != 'city':
                    end[key] = address[key]
            if address['city']:
                end['city'] = address['city']['name']
                end['state'] = address['city']['state']['uf']
                if address['is_parent'] == 1:
                    startup['Cidade'] = address['city']['name']
                    startup['Estado'] = address['city']['state']['uf']
            address_list.append(end)

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
}

same_name = ['Site', 'Setor SB', 'Badges', 'Cidade', 'Estado', 'Facebook',
             'Twitter', 'Instagram', 'Youtube', 'App (Play Store)', 'App (App Store)', 'Medium']

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