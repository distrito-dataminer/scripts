#! python3
# dataComplete.py - Completa um CSV de Startups com informações presentes em outro, sem substituí-las
# Uso: python dataComplete.py [csv mestre] [csv de enriquecimento] [Opcional: coluna-chave (padrão: "Site")]
# Exemplo: python dataComplete.py base.csv Startup

import sys, csv, re
from collections import OrderedDict
from unidecode import unidecode
from utils import cleaner, ddmdata

# Popula um dicionário com as informações do CSV mestre
master_list = ddmdata.readcsv(sys.argv[1])

# Popula um dicionário com as informações do CSV slave
slave_list = ddmdata.readcsv(sys.argv[2])

noAdd = False

if len(sys.argv) == 4:
    if sys.argv[3] == 'noadd':
        noAdd = True

# Limpa os dados de ambas as listas
master_list = cleaner.clean(master_list)
slave_list = cleaner.clean(slave_list)
output_filename = sys.argv[1].replace('.csv', '')+'_PLUS_'+sys.argv[2]

master_list = ddmdata.data_complete(master_list, slave_list)

master_list = cleaner.clean(master_list)

ddmdata.writecsv(master_list, output_filename)

print("\nOPERAÇÃO CONCLUÍDA.")