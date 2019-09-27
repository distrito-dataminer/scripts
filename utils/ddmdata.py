#! python3
# ddmdata.py - functions related to working with data

import csv
import itertools
import ast
from . import enrich
from more_itertools import unique_everseen as unique
from collections import OrderedDict

# Popula um dicionário com as informações do CSV


def readcsv(csvpath):
    startupList = []
    with open(csvpath, encoding="utf8") as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            startupList.append(row)
        fh.close()
    return startupList



def writecsv(startupList, csvpath='output.csv'):
    all_keys = []
    for item in startupList:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)
    outputFile = open(csvpath, 'w', newline='', encoding="utf8")
    outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
    outputWriter.writeheader()
    outputWriter.writerows(startupList)



def dict_from_csv(csvpath):
    reader = csv.reader(open(csvpath, 'r', encoding='utf8'))
    d = dict(reader)
    return d



def idict_from_csv(csvpath):
    reader = csv.reader(open(csvpath, 'r', encoding='utf8'))
    d = dict(reader)
    inverted_d = dict(map(reversed, d.items()))
    return inverted_d



def data_complete(master_list, slave_list, dictkey='Site', no_add=True):
    
    for master in master_list:
        if 'ID' in master and int(master['ID']) > last_id:
            last_id = int(master['ID'])
        clean_master_key = master[dictkey].replace('http://', '').lower()
        if clean_master_key == '':
            continue
        for slave in slave_list:
            clean_slave_key = slave[dictkey].replace('http://', '').lower()
            if clean_slave_key == '':
                continue
            if clean_master_key == clean_slave_key or clean_master_key in clean_slave_key or clean_slave_key in clean_master_key:
                slave['Found'] = 'YES'
                for key in master:
                    if key in slave:
                        if slave[key] != "":
                            if master[key] == "":
                                master[key] = slave[key]
                                print("Completando {} da {} com valor {}".format(
                                    key.upper(), master["Startup"].upper(), slave[key]))

    if no_add == False:
        new_startups = []
        print("\nAs startups a seguir não foram encontradas na base e estão sendo adicionadas:\n")
        for slave in slave_list:
            if 'Found' not in slave:
                print(slave['Startup'])
                new_startups.append(slave)

        for startup in new_startups:
            clean_startup = OrderedDict()
            for key in master_list[0]:
                clean_startup[key] = ""
            for key in startup:
                if key in clean_startup:
                    clean_startup[key] = startup[key]
            if 'ID' in clean_startup and last_id != 0:
                startup['ID'] = last_id + 1
                last_id += 1
            master_list.append(clean_startup)

    return master_list



def data_replace(master_list, slave_list, dictkey='Site', no_add=False):

    add_list = ['Descrição', 'Tags', 'Setor']
    last_id = 0
    
    for master in master_list:
        if 'ID' in master and int(master['ID']) > last_id:
            last_id = int(master['ID'])
        clean_master_key = master[dictkey].replace('http://', '').lower().replace(' ', '')
        if clean_master_key == '':
            continue
        for slave in slave_list:
            clean_slave_key = slave[dictkey].replace('http://', '').lower().replace(' ', '')
            if clean_slave_key == '':
                continue
            if clean_master_key == clean_slave_key:
                slave['Found'] = 'YES'
                for key in master:
                    if key in slave and slave[key] != '':
                        if key in add_list and master[key] != '':
                            current_list = master[key].split(',')
                            new_list = master[key].split(',')
                            final_list = list(unique(current_list + new_list))
                            if key == 'Descrição':
                                master[key] = '\n\n'.join(final_list)
                            else:
                                master[key] = ','.join(final_list)
                            print("Completando {} da {} com valor {}".format(
                                key.upper(), master["Startup"].upper(), ','.join(final_list)))
                        else:
                            master[key] = slave[key]
                            print("Completando {} da {} com valor {}".format(
                                key.upper(), master["Startup"].upper(), slave[key]))

    if no_add == False:
        new_startups = []
        print("\nAs startups a seguir não foram encontradas na base e estão sendo adicionadas:\n")
        for slave in slave_list:
            if 'Found' not in slave:
                print(slave['Startup'])
                new_startups.append(slave)

        for startup in new_startups:
            clean_startup = OrderedDict()
            for key in master_list[0]:
                clean_startup[key] = ""
            for key in startup:
                if key in clean_startup:
                    clean_startup[key] = startup[key]
            if 'ID' in clean_startup and last_id != 0:
                clean_startup['ID'] = last_id + 1
                last_id += 1
            master_list.append(clean_startup)

    return master_list



def lkd_merge(startup_list, lkd_list):
    address_list = []
    for startup in startup_list:
        for lkd in lkd_list:
            if startup['LinkedIn'] == lkd['url'].replace("https://www.", "http://"):
                if lkd['logo'] != '':
                    startup['Logo LKD'] = lkd['logo']
                if lkd['follower_count'] != '':
                    startup['Seguidores LKD'] = lkd['follower_count']
                if lkd['description'] != '':
                    if 'Descrição' in startup:
                        if lkd['description'] not in startup['Descrição']:
                            startup['Descrição'] += '\n\n' + lkd['description']
                    else:
                        startup['Descrição'] = lkd['description']
                if lkd['name'] != '':
                    startup['Nome LKD'] = lkd['name']
                if lkd['company_size'] != '':
                    startup['Faixa # de funcionários'] = lkd['company_size']
                if lkd['founded_year'] != '' or (lkd['founded_year'] != '' and startup['Ano de Fundação'] == ''):
                    startup['Ano de fundação'] = lkd['founded_year']
                if lkd['cover_image'] != '':
                    startup['Foto de capa'] = lkd['cover_image']
                if 'Cidade' not in startup or (lkd['city'] != '' and startup['Cidade'] == ''):
                    startup['Cidade'] = lkd['city']
                if 'Estado' not in startup or (lkd['state'] != '' and startup['Estado'] == ''):
                    startup['Estado'] = lkd['state']
                if 'País' not in startup or (lkd['country'] != '' and startup['País'] == ''):
                    startup['País'] = lkd['country']
                if lkd['number_of_self_declared_employees'] != '':
                    startup['Funcionários LKD'] = lkd['number_of_self_declared_employees']
                if lkd['tags'] != '':
                    lkdtags = ast.literal_eval(lkd['tags'])
                    if 'Tags' in startup:
                        oldtags = startup['Tags'].split(',')
                        newtags = unique(lkdtags + oldtags)
                        startup['Tags'] = ','.join(newtags)
                    else:
                        startup['Tags'] = ','.join(lkdtags)
                if lkd['confirmed_locations']:
                    locations = ast.literal_eval(lkd['confirmed_locations'])
                    if 'line1' in locations[0]:
                        keysArray = ['line1', 'line2', 'city',
                                     'geographicArea', 'postalCode']
                        addlines = [locations[0][x]
                                    for x in keysArray if x in locations[0]]
                        address = ''
                        for i in range(len(addlines)):
                            address += ', ' + addlines[i]
                        address = address.strip().strip(',').strip()
                        startup['Endereço'] = address
                    for location in locations:
                        if ('line1' or 'line2') in location:
                            newLoc = enrich.lkd_address(location, startup)
                            address_list.append(newLoc)
    return startup_list, address_list



def startups_from_lkd(lkd_list):
    startup_list = []
    for lkd_info in lkd_list:
        if lkd_info['name'] and lkd_info['url'] and lkd_info['website']:
            startup = {'Fonte': 'LinkedIn'}
            startup['Startup'] = lkd_info['name']
            startup['LinkedIn'] = lkd_info['url']
            startup['Site'] = lkd_info['website']
            startup_list.append(startup)
    startup_list, address_list = lkd_merge(startup_list, lkd_list)
    return startup_list, address_list



def startups_from_crunchbase(cb_list):
    startup_list = []
    cb_dict = {
        'Organization Name': 'Startup',
        'Website': 'Site',
        'LinkedIn': 'LinkedIn',
        'Organization Name URL': 'Crunchbase',
    }
    for cb_info in cb_list:
        startup = {'Fonte': 'Crunchbase'}
        for key, value in cb_dict.items():
            if key in cb_info:
                startup[value] = cb_info[key]
        location = [cb.strip()
                    for cb in cb_info['Headquarters Location'].split(',')]
        if len(location) == 3:
            startup['Cidade'], startup['Estado'], startup['País'] = location
        if cb_info['Founded Date']:
            startup['Ano de fundação'] = cb_info['Founded Date'][0:4]
        startup_list.append(startup)
    return startup_list



def startups_from_startupbase(sb_list):
    startup_list = []
    null_list = ['S/N', 'null']

    sb_dict = {
        'Nome': 'Startup',
        'site-href': 'Site',
        'linkedin': 'LinkedIn',
        'ano': 'Ano de fundação',
        'publico': 'Público',
        'modelo': 'Modelo de negócio',
        'momento': 'Estágio da operação',
        'tamanho': 'Porte SB',
        'facebook': 'Facebook',
        'descricao': 'Descrição',
        'twitter': 'Twitter',
        'instagram': 'Instagram',
        'crunchbase': 'Crunchbase',
        'link-href': 'StartupBase',
        'update': 'Última atualização SB',
        'verified': 'Verified SB',
        'Setor': 'Setor SB',
    }

    for sb_info in sb_list:
        
        startup = {'Fonte': 'StartupBase'}

        for key, value in sb_dict.items():
            if key in sb_info:
                if sb_info[key] in null_list:
                    startup[value] = ''
                else:
                    startup[value] = sb_info[key]

        if sb_info['Local']:
            location = [sb.strip() for sb in sb_info['Local'].split('-')]
            if len(location) == 2:
                startup['Cidade'], startup['Estado'] = location

        if sb_info['tags']:
            tag_list = eval(sb_info['tags'])
            final_tag_list = []
            for tag in tag_list:
                if 'tags' in tag:
                    final_tag_list.append(tag['tags'])
            startup['Tags'] = ','.join(final_tag_list)

        startup_list.append(startup)

    return startup_list



def rd_convert(rd_list):
    
    conversion_dict = {'Email': 'E-mail',
                  'Telefone': 'Telefone',
                  'Estado': 'Estado',
                  'Cidade': 'Cidade',
                  'Ano de Fundação': 'Ano de fundação',
                  'CNPJ': 'CNPJ',
                  'Constituição Legal': 'Constituição Legal',
                  'Descrição do Produto / Serviço': 'Descrição',
                  'Estágio atual': 'Estágio da operação',
                  'Faixa de faturamento anual': 'Faturamento Presumido',
                  'LinkedIn Company Page da Startup': 'LinkedIn',
                  'Modelo de negócios': 'Modelo de negócio',
                  'Modelo do Público': 'Público',
                  'Nome Completo dos Fundadores': 'Founders',
                  'Número de funcionários da sua empresa': 'Faixa # de funcionários',
                  'Segmento da Startup': 'Setor',
                  'Site da Startup': 'Site',
                  'Startup': 'Startup'}

    sector_dict = {'Agtech (Agronegócio)': 'AgTech',
                'AdTech (Advertising, Marketing, Social, MarTech)': 'AdTech'}

    converted_list = []

    for startup in rd_list:
        converted_startup = {'Fonte': 'Cadastro DM', 'Checado': 'Cadastro DM'}
        for key in startup:
            if key in conversion_dict:
                converted_startup[conversion_dict[key]] = startup[key]
        if 'Setor' in converted_startup:
            if converted_startup['Setor'] in sector_dict:
                converted_startup['Setor'] = sector_dict[converted_startup['Setor']]
        converted_list.append(converted_startup)

    return converted_list