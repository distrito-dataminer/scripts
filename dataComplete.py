#! python3
# dataComplete.py - Completa um CSV de Startups com informações presentes em outro, sem substituí-las
# Uso: python dataComplete.py [csv mestre] [csv de enriquecimento] [Opcional: coluna-chave (padrão: "Site")]
# Exemplo: python dataComplete.py base.csv Startup

import sys, csv, re
from collections import OrderedDict
from unidecode import unidecode
from utils import cleaner, ddmdata

# Popula um dicionário com as informações do CSV mestre
masterSL = ddmdata.readcsv(sys.argv[1])

# Popula um dicionário com as informações do CSV slave
slaveSL = ddmdata.readcsv(sys.argv[2])

noAdd = False

if len(sys.argv) > 3:
    if sys.argv[3] == 'noadd':
        noAdd = True

# Limpa os dados de ambas as listas
masterSL = cleaner.clean(masterSL)
slaveSL = cleaner.clean(slaveSL)

# Cria um CSV com as colunas relevantes para servir de output
all_keys = masterSL[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()

for master in masterSL:
    for slave in slaveSL:
        if master['Site'] == slave['Site']:
            slave['Found'] = 'YES'
            for key in master:
                if key in slave:
                    if slave[key] != "":
                        if master[key] == "":
                            master[key] = slave[key]
                            print("Completando {} da {} com valor {}".format(key.upper(), master["Startup"].upper(), slave[key]))
    outputWriter.writerow(master)

if noAdd == False:
    print("\nAs startups a seguir não foram encontradas na base e estão sendo adicionadas:\n")
    newStartups = []
    for slave in slaveSL:
        if 'Found' not in slave:
            print(slave['Startup'])
            newStartups.append(slave)

    for startup in newStartups:
        cleanStartup = OrderedDict()
        for key in masterSL[0]:
            cleanStartup[key] = ""
        for key in startup:
            if key in cleanStartup:
                cleanStartup[key] = startup[key]
        outputWriter.writerow(cleanStartup)

outputFile.close()
print("\nOPERAÇÃO CONCLUÍDA.")