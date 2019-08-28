#! python3
# dataRefeed.py - retroalimenta dados de um estudo pra base
# Uso: dataRefeed.py [csv da base] [csv do estudo]

from utils import ddmdata, cleaner
import re, sys

base = ddmdata.readcsv(sys.argv[1])
estudo = ddmdata.readcsv(sys.argv[2])

base = cleaner.clean(base)
estudo = cleaner.clean(estudo)

#Parâmetros - altere conforme necessário
estudoName = "HealthTech"
ignoreFields = ['ID', 'ID Estudo', 'Tirar da base?', 'Remover do estudo?', 'Por que tirar?', 'Verificada', 'Logo', 'Leads Abbott']
addFields = ['Setor', 'E-mail', 'Tags', 'Categoria', 'Subcategoria']

def checkID(base, estudo):
    for estudada in estudo:
        if estudada['ID']:
            continue
        for startup in base:            
            if estudada['Site'] != '' and estudada['Site'] == startup['Site']:
                print("\nIgualando por site:")
                print(estudada['Startup'] + " --- " + estudada['Site'] + " --- " + estudada['LinkedIn'])
                print(startup['Startup'] + " --- " + startup['Site'] + " --- " + startup['LinkedIn'])
                estudada['ID'] = startup['ID']
                break
    for estudada in estudo:
        if estudada['ID']:
            continue
        for startup in base:
            if estudada['Startup'] != '' and estudada['Startup'] == startup['Startup']:
                print("\nIgualando por nome:")
                print(estudada['Startup'] + " --- " + estudada['Site'] + " --- " + estudada['LinkedIn'])
                print(startup['Startup'] + " --- " + startup['Site'] + " --- " + startup['LinkedIn'])
                estudada['ID'] = startup['ID']
    return base, estudo

def updateStartup(estudada, startup):
    startup['Checado'] = estudoName
    if estudada['Tirar da base?'] == 'TRUE':
        startup['Tirar?'] = estudada['Por que tirar?']
        return startup
    for key in estudada:
        if key not in ignoreFields and key not in addFields:
            if estudada['Remover do estudo?'] == 'TRUE':
                if estudada[key] != '':
                    startup[key] = estudada[key]
            else:
                startup[key] = estudada[key]
    for field in addFields:
        if field in estudada:
            currentList = startup[field].split(',')
            estudadaList = estudada[field].split(',')
            for item in estudadaList:
                if item not in currentList:
                    currentList.append(item)
                startup[field] = ','.join(currentList)
    if 'Descrição' in estudada and estudada['Descrição'] not in startup['Descrição']:
        startup['Descrição'] = startup['Descrição'] + '\n\n' + estudada['Descrição']
    return startup

base, estudo = checkID(base, estudo)

lastID = int(base[-1]['ID'])

for estudada in estudo:
    if 'Categoria' not in estudada:
        estudada['Categoria'] = ''
    if 'Subcategoria' not in estudada:
        estudada['Subcategoria'] = ''
    if estudada['Verificada'] == 'FALSE':
        continue
    if estudada['Tirar da base?'] == 'TRUE':
        if estudada['Por que tirar?'] == 'Duplicata':
            continue
    if estudada['ID']:
        for startup in base:
            if estudada['ID'] == startup['ID']:
                startup = updateStartup(estudada, startup)
    else:
        if estudada['Tirar da base?'] == 'FALSE' and estudada['Site'] != '':
            lastID += 1
            newStartup = {}
            newStartup['ID'] = lastID
            if estudada['Remover do estudo?'] == 'FALSE':
                newStartup['Checado'] = estudoName
            for key in estudada:
                if key not in ignoreFields:
                    newStartup[key] = estudada[key]
            base.append(newStartup)


base = cleaner.clean(base)
estudo = cleaner.clean(estudo)

ddmdata.writecsv(base, sys.argv[1].replace('.csv', '') + '_PLUS_'+ estudoName + '.csv')
ddmdata.writecsv(estudo, sys.argv[2].replace('.csv', '') + '_IDs_atualizadas.csv')