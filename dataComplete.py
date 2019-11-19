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

for master in master_list:
    for key in slave_list[0]:
        if key not in master:
            master[key] = ''

noAdd = False
replace = False
id_type = 'ID'

if len(sys.argv) > 3:
    if 'noadd' in sys.argv:
        noAdd = True
    if 'replace' in sys.argv:
        replace = True
    if 'estudo' in sys.argv:
        id_type = 'ID Estudo'

# Limpa os dados de ambas as listas
master_list = cleaner.clean(master_list)
slave_list = cleaner.clean(slave_list)
output_filename = sys.argv[1].replace('.csv', '')+'_PLUS_'+sys.argv[2]

if replace:
    master_list = ddmdata.data_replace(master_list, slave_list, no_add=noAdd, id_type=id_type, dictkey='ID')
else:
    master_list = ddmdata.data_complete(master_list, slave_list, no_add=noAdd, id_type=id_type, dictkey='ID')

master_list = cleaner.clean(master_list)

ddmdata.writecsv(master_list, output_filename)

print("\nOPERAÇÃO CONCLUÍDA.")