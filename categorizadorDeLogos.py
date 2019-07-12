#! python3
# coding: utf-8
# categorizadorDeLogos.py - categoriza arquivos em pastas de acordo com categoria e subcategoria
# Uso: python categorizadorDeLogos.py [csv] [pasta dos logos] [pasta destino]
# Exemplo: python categorizadorDeLogos.py C:\logos.csv C:\test\ C:\test2\
# O CSV deve ter colunas chamadas 'Startup', 'Categoria', 'Subcategoria', e 'Site'

import re, csv, os, shutil, sys, unidecode
from utils import ddmdata

# Informa o usuário do uso correto caso os argumentos não sejam passados
if len(sys.argv) != 4:
    print(r"Uso: python categorizadorLogos.py [csv] [pasta com logos] [pasta destino]")
    print(r"Exemplo: python categorizadorDeLogos.py C:\logos.csv C:\test\ C:\test2\\")
    sys.exit()

# Garante que os paths vão terminar com \    
path = sys.argv[2]
if path[-1] != "\\":
    path += "\\"

destpath = sys.argv[3]
if destpath[-1] != "\\":
    path += "\\"

# Lê o CSV e transforma numa lista de dicionários
file = sys.argv[1]
startupList = []
with open(file, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)

# Cria uma lista de todos os arquivos presentes na pasta (assumindo ser os logos)for filename in os.listdir(path):
logoList = []
for filename in os.listdir(path):
    logoList.append(filename)

# Inicializa variáveis usadas adiante
foundList = []
foundLogos = []
notFoundList = []
notFoundLogos = []
found = False

# Roda todas as startups do CSV, procura um logo correspondente para cada uma e copia para a pasta correta se achar
for a in startupList:
    found = False
    if not os.path.exists(destpath+a['Categoria']+"\\"+a['Subcategoria']):
        os.makedirs(destpath+a['Categoria']+"\\"+a['Subcategoria'])
    r = re.compile("^"+unidecode.unidecode(a['Startup'].lower().replace(" ", ""))+r"\..*?$")
    for b in logoList:
        mo = r.search(unidecode.unidecode(b.lower().replace(" ", "")))
        if mo == None:
            continue
        print("Found match for " + a['Startup'] +":      " + b)
        shutil.copy(path+b, destpath+a['Categoria']+"\\"+a['Subcategoria'])
        foundList.append(a['Startup'])
        a['Logo'] = 'TRUE'
        foundLogos.append(b)
        found = True
    if found == False:
        print("Match not found for: " + a['Startup'])
        notFoundList.append(a)

# Encontra e lista todos os logos que ficaram sem categoria e todas as startups que ficaram sem logo
notFoundLogos = [item for item in logoList if item not in foundLogos]
print("\n\n\nLOGOS THAT COULD NOT BE CATEGORIZED:\n")
for logo in notFoundLogos:
    print(logo)
print("\n\n\nSTARTUPS THAT HAD NO LOGO:\n")
for startup in notFoundList:
    print(startup['Startup'].ljust(30) + startup['Site'])

ddmdata.writecsv(startupList, 'logoupdate.csv')

# Copia os logos que ficaram sem categoria para a pasta base do destino
if notFoundLogos != []:
    for notFound in notFoundLogos:
        shutil.copy(path+notFound, destpath)
