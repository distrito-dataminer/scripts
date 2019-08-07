#! python3
# linkToLoveMondays.py - Obtém URLs do LoveMondays a partir de uma lista de sites por meio do Google Custom Search
# Uso - python linkToLoveMondays.py [csv] [opcional: noreplace] <- não substitui informações já presentes no csv
# Exemplo: python linkToLoveMondays.py startups.csv noreplace

import sys, csv, shutil, datetime, re
from googleapiclient.discovery import build

from utils import ddmdata, privatekeys

lmRegex = re.compile(r'https?:\/\/www.lovemondays.com.br\/trabalhar-na-.+?\/avaliacoes')

# Conecta na API do Google com a chave de API providenciada
service = build("customsearch", "v1", developerKey=privatekeys.devkey)

noReplace = False

if len(sys.argv) > 2 and sys.argv[2].lower() == "noreplace":
    noReplace = True

# Popula um dicionário com os dados de startups do csv
startupList = ddmdata.readcsv(sys.argv[1])

# Faz uma busca com o site da startup como query no LoveMondays
for startup in startupList:
    if (noReplace == True) and "LoveMondays" in startup.keys():
        if (startup['LoveMondays'] != ("" or "null")):
            print("LoveMondays for " + startup['Startup'] + " already present.\n")
            continue
    print("Getting LoveMondays for " + startup['Startup'] + "...")
    res = service.cse().list(
      q='trabalhar na {}'.format(startup['Startup']),
      cx='002626537913979718585:gccyl859xhm',
      num = 10,
    ).execute()
    if 'items' not in res.keys():
        print("No results. \n")
        result = "NÃO ENCONTRADO"
    else:
        for item in res['items']:
            mo = re.search(lmRegex, item['link'])
            if mo:
                result = mo.group()
                print("Found LoveMondays: " + result + '\n')
                break
    startup['LoveMondays'] = result

# Fecha o arquivo e renomeia para evitar substituição
ddmdata.writecsv(startupList, sys.argv[1].replace('.csv', '') + '_loveMondays.csv')