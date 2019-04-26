#! python3
# dataCleaner.py - Limpa dados de um CSV para mantê-los no padrão Dataminer
# Dados limpos atualmente: CNPJ, Site, LinkedIn, Facebook, Instagram, Twitter, Crunchbase
# Uso: python dataCleaner.py [csv]
# Exemplo: python dataCleaner.py base.csv

import sys, csv, re
from collections import OrderedDict
from unidecode import unidecode

siglas = {
    "acre": "AC",
    "alagoas": "AL",
    "amapa": "AP",
    "amazonas": "AM",
    "bahia": "BA",
    "ceara": "CE",
    "distritofederal": "DF",
    "espiritosanto": "ES",
    "goias": "GO",
    "maranhao": "MA",
    "matogrosso": "MT",
    "matogrossodosul": "MS",
    "minasgerais": "MG",
    "para": "PA",
    "paraiba": "PB",
    "parana": "PR",
    "pernambuco": "PE",
    "piaui": "PI",
    "riodejaneiro": "RJ",
    "riograndedonorte": "RN",
    "riograndedosul": "RS",
    "rondonia": "RO",
    "roraima": "RR",
    "santacatarina": "SC",
    "saopaulo": "SP",
    "sergipe": "SE",
    "tocantins": "TO"
}

# Popula um dicionário com as informações do CSV
startupList = []
with open(sys.argv[1], encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)
    fh.close()

# Cria um CSV com as colunas relevantes para servir de output
all_keys = startupList[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()

for startup in startupList:

# Limpa o CNPJ, adicionando 0s que o Excel come e tirando símbolos
    if 'CNPJ' in startup:
        if (startup['CNPJ'] != "") and (startup['CNPJ'] != "null"):
            newCnpj = re.sub(r'[^\d]', '', startup['CNPJ'])
            newCnpj = newCnpj.zfill(14)
            if newCnpj != '00000000000000':
                newCnpj = "{}.{}.{}/{}-{}".format(newCnpj[:2],newCnpj[2:5],newCnpj[5:8],newCnpj[8:12],newCnpj[12:14])
                startup['CNPJ'] = newCnpj
            else:
                startup['CNPJ'] = ""

# Limpa o site, mantendo formato consistente e letras minúsculas
    if 'Site' in startup:
        if (startup['Site'] != "") and (startup['Site'] != "null"):
            newSite = startup['Site'].lower().replace("https://", "http://")
            if "http://" not in newSite:
                newSite = "http://" + newSite
            newSite = newSite.replace("www.", "")
            siteRegex = re.compile(r"http:\/\/[^\/&?]*", re.IGNORECASE)
            mo = siteRegex.search(newSite)
            if mo != None:
                newSite = mo.group().lower().strip()
            startup['Site'] = newSite.strip().strip('/').lower()

# Limpa o URL do LinkedIn
    if 'LinkedIn' in startup:
        if (startup['LinkedIn'] != "") and (startup['LinkedIn'] != "null") and ("[" not in startup['LinkedIn']):
            newLkd = startup['LinkedIn'].lower()
            lkdRegex = re.compile(r"linkedin\.com\/company\/[^\/&?]*", re.IGNORECASE)
            mo = lkdRegex.search(newLkd)
            if mo != None:
                newLkd = "http://" + mo.group().lower().strip()
                startup['LinkedIn'] = newLkd

# Limpa o URL do Facebook
    if 'Facebook' in startup:
        if (startup['Facebook'] != "") and (startup['Facebook'] != "null") and ("[" not in startup['Facebook']):
            newFb = startup['Facebook'].lower()
            fbRegex = re.compile(r"facebook\.com\/(pg\/|page\/|pages\/)?[^\/?&\.]*", re.IGNORECASE)
            mo = fbRegex.search(newFb)
            if mo != None:
                newFb = "http://" + mo.group().lower().strip()
                startup['Facebook'] = newFb

# Limpa o URL do Twitter
    if 'Twitter' in startup:
        if (startup['Twitter'] != "") and (startup['Twitter'] != "null") and ("[" not in startup['Twitter']):
            newTt = startup['Twitter'].lower()
            ttRegex = re.compile(r"twitter\.com\/company\/[^\/&?]*", re.IGNORECASE)
            mo = ttRegex.search(newTt)
            if mo != None:
                newTt = "http://" + mo.group().lower().strip()
                startup['Twitter'] = newTt

# Limpa o URL do Instagram
    if 'Instagram' in startup:
        if (startup['Instagram'] != "") and (startup['Instagram'] != "null") and ("[" not in startup['Instagram']):
            newInsta = startup['Instagram'].lower()
            instaRegex = re.compile(r"instagram\.com\/[^&?\/].*", re.IGNORECASE)
            mo = instaRegex.search(newInsta)
            if mo != None:
                newInsta = "http://" + mo.group().lower().strip()
                startup['Instagram'] = newInsta

# Limpa o URL do Crunchbase
    if 'Crunchbase' in startup:
        if (startup['Crunchbase'] != "") and (startup['Crunchbase'] != "null") and ("[" not in startup['Crunchbase']):
            newCb = startup['Crunchbase'].lower()
            cbRegex = re.compile(r"instagram\.com\/[^&?\/].*", re.IGNORECASE)
            mo = cbRegex.search(newCb)
            if mo != None:
                newCb = "http://" + mo.group().lower().strip()
                startup['Crunchbase'] = newCb

# Transforma o Estado em sigla
    if 'Estado' in startup:
        if unidecode(startup['Estado'].lower().replace(" ", "")) in siglas.keys():
            startup['Estado'] = siglas[unidecode(startup['Estado'].lower().replace(" ", ""))]

# Tira newlines e substitui por vírgulas pra separar mais de um item por célula
    exceptionList = ["Descrição"]
    for key in startup:
        if key not in exceptionList:
            startup[key] = startup[key].replace("\n", ",")

    outputWriter.writerow(startup)

print("Pronto!")
outputFile.close()