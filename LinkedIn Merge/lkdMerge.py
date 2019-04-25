#! python3
# lkdMerge.py - Depois de rodar o bot de LinkedIn, anexa as informações de volta à planilha original
import csv, re, sys, os, shutil

startupcsv = sys.argv[1]
lkdcsv = sys.argv[2]

startupList = []
lkdList = []

with open(startupcsv, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)
    fh.close()

with open(lkdcsv, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        lkdList.append(row)
    fh.close()

keys = []

for startup in startupList:
    for lkd in lkdList:
        if startup['LinkedIn'] == lkd['url'].replace("https://www.", "http://"):
            if lkd['logo'] != '':
                startup['Logo LKD'] = lkd['logo']
            if lkd['follower_count'] != '':
                startup['Seguidores LKD'] = lkd['follower_count']
            if lkd['description'] != '':
                startup['Descrição'] = lkd['description']
            if lkd['name'] != '':
                startup['Nome LKD'] = lkd['name']
            if lkd['company_size'] != '':
                startup['Faixa # de funcionários'] = lkd['company_size']
            if lkd['founded_year'] != '':
                startup['Ano de fundação'] = lkd['founded_year']
            if lkd['cover_image'] != '':
                startup['Foto de capa'] = lkd['cover_image']
            if lkd['city'] != '':
                startup['Cidade'] = lkd['city']
            if lkd['state'] != '':
                startup['Estado'] = lkd['state']
            if lkd['country'] != '':
                startup['País'] = lkd['country']
            if lkd['number_of_self_declared_employees'] != '':
                startup['Funcionários LKD'] = lkd['number_of_self_declared_employees']
            if lkd['tags'] != '':
                startup['Tags'] = lkd['tags']
    for key in startup:
        if key not in keys:
            keys.append(key)   

outputFile = open('mergedOutput.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, keys, delimiter=',')
outputWriter.writeheader()
outputWriter.writerows(startupList)