#! python3
# dataRefeed.py - retroalimenta dados de um estudo pra base
# Uso: dataRefeed.py [csv da base] [csv do estudo]

from utils import ddmdata, cleaner
import re, sys

base = ddmdata.readcsv(sys.argv[1])
estudo = ddmdata.readcsv(sys.argv[2])
estudoName = sys.argv[3]

base = cleaner.clean(base)
estudo = cleaner.clean(estudo)

for estudada in estudo:
    if 'ID' not in estudada:
        estudada['ID'] = ''
    if 'LinkedIn' not in estudada:
        estudada['LinkedIn'] = ''

#Parâmetros - altere conforme necessário
ignoreFields = ['ID', 'ID Estudo', 'Tirar da base?', 'Remover do estudo?', 'Por que tirar?', 'Verificada', 'Logo', 'Leads Abbott', 'Check', 'Match count', 'Atenção especial', 'Setor Base', 'Matched in', 'Matched for', 'TOP']
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
                #startup['Site'] = estudada['Site']
                estudada['ID'] = startup['ID']
                break
    return base, estudo

def updateStartup(estudada, startup):
    if estudada['Tirar da base?'] == 'TRUE':
        startup['Tirar?'] = estudada['Por que tirar?']
        startup['Checado'] = estudoName
        return startup
    if estudada['Remover do estudo?'] == 'FALSE':
        startup['Checado'] = estudoName
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
                if item != '' and item not in currentList:
                    currentList.append(item)
            currentList = [item for item in currentList if item != '']
            startup[field] = ','.join(currentList)
    if 'Descrição' in estudada and estudada['Descrição'] not in startup['Descrição']:
        startup['Descrição'] = startup['Descrição'] + '\n\n' + estudada['Descrição']
    if estudada['Por que tirar?'] == 'Não é EdTech':
            setores = startup['Setor'].split(',')
            while 'Educação' in setores:
                setores.remove('Educação')
            while 'EdTech' in setores:
                setores.remove('EdTech')
            startup['Setor'] = ','.join(setores)
    return startup

base, estudo = checkID(base, estudo)
ddmdata.writecsv(estudo, sys.argv[2].replace('.csv', '') + '_IDs_atualizadas.csv')

lastID = 0
for startup in base:
    if int(startup['ID']) > lastID:
        lastID = int(startup['ID'])

new_count = 0

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
        if estudada['Site'] != '':
            lastID += 1
            newStartup = {}
            newStartup['ID'] = lastID
            estudada['ID'] = lastID
            if estudada['Remover do estudo?'] == 'FALSE' or estudada['Tirar da base?'] == 'TRUE':
                newStartup['Checado'] = estudoName
            if estudada['Tirar da base?'] == 'TRUE':
                newStartup['Tirar?'] = estudada['Por que tirar?']
            for key in estudada:
                if key not in ignoreFields:
                    newStartup[key] = estudada[key]
            base.append(newStartup)
            print('\nAdicionando nova startup: {}'.format(estudada['Startup']))
            new_count += 1

print('\n{} novas startups adicionadas!'.format(new_count))

for startup in base:
    for key in base[0].keys():
        if key not in startup:
            startup[key] = ''

base = cleaner.score(cleaner.clean(base))
estudo = cleaner.clean(estudo)

ddmdata.writecsv(estudo, sys.argv[2].replace('.csv', '') + '_IDs_atualizadas.csv')
ddmdata.writecsv(base, sys.argv[1].replace('.csv', '') + '_PLUS_'+ estudoName + '.csv')
