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
from utils import cleaner, ddmdata

# Popula um dicionário com as informações do CSV
startupList = ddmdata.readcsv(sys.argv[1])

score = False
if len(sys.argv) > 2:
    if sys.argv[2].lower() == "score":
        score = True

# Limpa os dados
startupList = cleaner.clean(cleaner.clean(cleaner.clean(startupList)))

# Pontua o nível de preenchimento se essa opção estiver ligada
if score == True:
    startupList = cleaner.score(startupList)

# Cria um CSV com as colunas relevantes para servir de output e escreve os dados limpos
ddmdata.writecsv(startupList, sys.argv[1].replace('.csv','')+'_clean.csv')

print("Pronto!")
