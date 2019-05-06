#! python3
# dataComplete.py - Completa um CSV de Startups com informações presentes em outro, sem substituí-las
# Uso: python dataCleaner.py [csv mestre] [csv de enriquecimento] [Opcional: coluna-chave (padrão: "Site")]
# Exemplo: python dataCleaner.py base.csv Nome

import sys, csv, re
from collections import OrderedDict
from unidecode import unidecode

# Popula um dicionário com as informações do CSV mestre
masterSL = []
with open(sys.argv[1], encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        masterSL.append(row)
    fh.close()

# Popula um dicionário com as informações do CSV slave
slaveSL = []
with open(sys.argv[2], encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        slaveSL.append(row)
    fh.close()

# Cria um CSV com as colunas relevantes para servir de output
all_keys = masterSL[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()

for master in masterSL:
    for slave in slaveSL:
        if master["Site"] == slave["Site"]:
            for key in master:
                if key in slave:
                    if slave[key] != "":
                        if master[key] == "":
                            master[key] = slave[key]
                            print("Completando {} da {} com valor {}".format(key.upper(), master["Nome"].upper(), slave[key]))
    outputWriter.writerow(master)


outputFile.close()
print("Pronto.")