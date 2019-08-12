#! python3
# lkdMerge.py - Depois de rodar o bot de LinkedIn, anexa as informações de volta à planilha original
import csv, re, sys, os, shutil, ast
from utils import cleaner, ddmdata, enrich, privatekeys, sanity
from more_itertools import unique_everseen as unique

startupcsv = sys.argv[1]
lkdcsv = sys.argv[2]

startupList = ddmdata.readcsv(startupcsv)
lkdList = ddmdata.readcsv(lkdcsv)

startupList = cleaner.clean(startupList)

addresslist = []

for startup in startupList:
    for lkd in lkdList:
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
            if lkd['founded_year'] != '':
                startup['Ano de fundação'] = lkd['founded_year']
            if lkd['cover_image'] != '':
                startup['Foto de capa'] = lkd['cover_image']
            if 'Cidade' not in startup or lkd['city'] != '' and startup['Cidade']:
                startup['Cidade'] = lkd['city']
            if 'Estado' not in startup or lkd['state'] != '' and startup['Estado'] == '':
                startup['Estado'] = lkd['state']
            if 'País' not in startup or lkd['country'] != '' and startup['País'] == '':
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
                    keysArray = ['line1', 'line2', 'city', 'geographicArea', 'postalCode']
                    addlines = [locations[0][x] for x in keysArray if x in locations[0]]
                    address = ''
                    for i in range(len(addlines)):
                        address += ', ' + addlines[i]
                    address = address.strip().strip(',').strip()
                    startup['Endereço'] = address
                for location in locations:
                    if ('line1' or 'line2') in location:
                        newLoc = enrich.lkdAdd(location, startup)
                        addresslist.append(newLoc)

startupList = cleaner.clean(cleaner.clean((startupList)))

ddmdata.writecsv(startupList, '{}_lkd_merged.csv'.format(startupcsv.replace('.csv', '')))
ddmdata.writecsv(addresslist, '{}_lkd_addresses.csv'.format(startupcsv.replace('.csv', '')))