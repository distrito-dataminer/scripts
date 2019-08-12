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
estudoName = "ParanáTech"
ignoreFields = ['ID', 'ID Estudo', 'Tirar da base?', 'Remover do estudo?', 'Por que tirar?', 'Verificada', 'Logo']
addFields = ['Setor', 'E-mail', 'Tags', 'Descrição']

def checkID(base, estudo):
    for estudada in estudo:
        if estudada['ID']:
            continue
        for startup in base:
            if estudada['Site'] == startup['Site']:
                print("\nIgualando por site:")
                print(estudada['Startup'] + " --- " + estudada['Site'] + " --- " + estudada['LinkedIn'])
                print(startup['Startup'] + " --- " + startup['Site'] + " --- " + startup['LinkedIn'])
                estudada['ID'] = startup['ID']
                break
    for estudada in estudo:
        if estudada['ID']:
            continue
        for startup in base:
            if estudada['Startup'] == startup['Startup']:
                print("\nIgualando por nome:")
                print(estudada['Startup'] + " --- " + estudada['Site'] + " --- " + estudada['LinkedIn'])
                print(startup['Startup'] + " --- " + startup['Site'] + " --- " + startup['LinkedIn'])
                estudada['ID'] = startup['ID']
    return base, estudo

def updateStartup(estudada, startup):
    startup['Checado'] = estudoName
    for key in estudada:
        if key not in ignoreFields and key not in addFields:
            startup[key] = estudada[key]
    for field in addFields:
        currentList = startup[field].split(',')
        estudadaList = estudada[field].split(',')
        for item in estudadaList:
            if item not in currentList:
                currentList.append(item)
        if field == 'Descrição':
            startup[field] = '\n'.join(currentList)
        else:
            startup[field] = ','.join(currentList)
    if estudada['Tirar da base?'] == 'TRUE':
        startup['Tirar?'] = estudada['Por que tirar?']
    return startup

base, estudo = checkID(base, estudo)

lastID = int(base[-1]['ID'])

for estudada in estudo:
    if estudada['Verificada'] == 'FALSE':
        continue
    if estudada['ID']:
        for startup in base:
            if estudada['ID'] == startup['ID']:
                startup = updateStartup(estudada, startup)
    else:
        lastID += 1
        newStartup = {}
        newStartup['ID'] = lastID
        newStartup['Checado'] = estudoName
        for key in estudada:
            if key not in ignoreFields:
                newStartup[key] = estudada[key]
        base.append(newStartup)

ddmdata.writecsv(base, sys.argv[1].replace('.csv', '') + '_PLUS_'+ estudoName + '.csv')
ddmdata.writecsv(estudo, sys.argv[2].replace('.csv', '') + '_IDs_atualizadas.csv')
