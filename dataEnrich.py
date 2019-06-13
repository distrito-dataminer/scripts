#! python3
# dataEnrich.py - Enriquece dados de empresas a partir de um CSV de CNPJs

import sys
import csv
import re
import requests
import pprint
from collections import OrderedDict

from unidecode import unidecode

from utils import cleaner, enrich, scoring, ddmdata
from utils.privatekeys import tokenTU as token

# Popula um dicionário com as informações do CSV
startupList = ddmdata.readcsv(sys.argv[1])

# Limpa os dados, roda o enriquecimento e limpa os dados novamente
startupList = cleaner.clean(startupList)
startupList, errorList, enderecoList = enrich.enrich(startupList)
startupList = cleaner.clean(startupList)

# Cria um CSV com as colunas relevantes para servir de output e escreve os dados limpos
filename = (sys.argv[1].replace('.csv', '') + '_enriquecida.csv')
ddmdata.writecsv(startupList, filename)

filename = (sys.argv[1].replace('.csv', '') + '_endereços.csv')
ddmdata.writecsv(enderecoList, filename)

# Cria um CSV com as startups que deram erro, caso existam
if len(errorList) > 0:
    filename = '{}_errors.csv'.format(sys.argv[1].replace('.csv', ''))
    ddmdata.writecsv(errorList, filename)
    print('De {} startups, {} apresentaram erro e estão em {}'.format(len(startupList), len(errorList), filename))