#! python3
# dataEnrich.py - Enriquece dados de empresas a partir de um CSV de CNPJs

import sys
import csv
import re
import requests
import pprint
from collections import OrderedDict

from unidecode import unidecode

from utils import cleaner, enrich, ddmdata
from utils.privatekeys import tokenTU as token

# Popula um dicionário com as informações do CSV
startup_list = ddmdata.readcsv(sys.argv[1])

# Limpa os dados, roda o enriquecimento e limpa os dados novamente
startup_list = cleaner.clean(startup_list)
startup_list, error_list, endereco_list = enrich.enrich(startup_list)
startup_list = cleaner.clean(startup_list)

# Cria um CSV com as colunas relevantes para servir de output e escreve os dados limpos
filename = (sys.argv[1].replace('.csv', '') + '_enriquecida.csv')
ddmdata.writecsv(startup_list, filename)

filename = (sys.argv[1].replace('.csv', '') + '_endereços.csv')
ddmdata.writecsv(endereco_list, filename)

# Cria um CSV com as startups que deram erro, caso existam
if len(error_list) > 0:
    filename = '{}_errors.csv'.format(sys.argv[1].replace('.csv', ''))
    ddmdata.writecsv(error_list, filename)
    print('De {} startups, {} apresentaram erro e estão em {}'.format(len(startup_list), len(error_list), filename))
