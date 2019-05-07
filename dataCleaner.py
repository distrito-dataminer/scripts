#! python3
# dataCleaner.py - Limpa dados de um CSV para mantê-los no padrão Dataminer
# Dados limpos atualmente: CNPJ, Site, LinkedIn, Facebook, Instagram, Twitter, Crunchbase
# Uso: python dataCleaner.py [csv]
# Exemplo: python dataCleaner.py base.csv

import sys
import csv
import re
from collections import OrderedDict
from unidecode import unidecode
from utils import cleaner, scoring

# Popula um dicionário com as informações do CSV
startupList = []
with open(sys.argv[1], encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)
    fh.close()

if len(sys.argv) > 2:
    if sys.argv[2].lower() == "score":
        score = True

# Limpa os dados
startupList = cleaner.clean(startupList)

# Pontua o nível de preenchimento se essa opção estiver ligada
if score == True:
    scoring.ndp(startupList)

# Cria um CSV com as colunas relevantes para servir de output e escreve os dados limpos
all_keys = startupList[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding="utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()
outputWriter.writerows(startupList)

print("Pronto!")
outputFile.close()