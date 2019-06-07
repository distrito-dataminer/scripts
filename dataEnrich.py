#! python3
# dataEnrich.py - Enriquece dados de empresas a partir de um CSV de CNPJs

import sys
import csv
import re
import requests
import pprint
from collections import OrderedDict
from unidecode import unidecode
from utils import cleaner, enrich, scoring

# Obtém o token de um arquivo de texto
token = open(r'.\utils\token.txt', 'r').read()

# Popula um dicionário com as informações do CSV
startupList = []
with open(sys.argv[1], encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)
    fh.close()

# Limpa os dados, roda o enriquecimento e limpa os dados novamente
startupList = cleaner.clean(startupList)
startupList, errorlist = enrich.enrich(startupList, token)
startupList = cleaner.clean(startupList)

# Cria um CSV com as colunas relevantes para servir de output e escreve os dados limpos
all_keys = []
for item in startupList:
    for key in item:
        if key not in all_keys:
            all_keys.append(key)
outputFile = open((sys.argv[1].replace('.csv', '') + '_enriquecida.csv'), 'w', newline='', encoding="utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()
outputWriter.writerows(startupList)
outputFile.close()

# Cria um CSV com as startups que deram erro, caso existam
if len(errorlist) > 0:
    all_error_keys = []
    for item in errorlist:   
        if key in item:
            if key not in all_error_keys:
                all_error_keys.append(key)
    errorFile = open((sys.argv[1].replace('.csv', '') + '_enriquecida_errors.csv'), 'w', newline='', encoding="utf8")
    errorWriter = csv.DictWriter(errorFile, all_error_keys, delimiter=',')
    errorWriter.writeheader()
    errorWriter.writerows(errorlist)
    errorFile.close()
    print('De {} startups, {} apresentaram erro e estão em {}'.format(len(startupList), len(errorlist), (sys.argv[1].replace('.csv', '') + '_enriquecida_errors.csv')))