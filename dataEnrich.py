#! python3
# dataEnrich.py - Popula um CSV com dados enriquecidos da TransUnion

import sys
import csv
import re
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

print(startupList[0].keys())
startupList = cleaner.clean(startupList)
startupList = enrich.enrich(startupList, token)

# Cria um CSV com as colunas relevantes para servir de output e escreve os dados limpos
all_keys = []
for startup in startupList:
    for key in startup:
        if key not in all_keys:
            all_keys.append(key)
outputFile = open('output.csv', 'w', newline='', encoding="utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()
outputWriter.writerows(startupList)