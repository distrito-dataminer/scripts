#! python3
# siteScraper.py - encontra informações relevantes de startups em sites contidos em um csv
# Informações coletadas: CNPJ, LinkedIn, Facebook, Instagram, Twitter, Crunchbase
# O csv deve conter pelo menos as colunas 'Nome' e 'Site'.
# Uso: python cnpjScraper.py [csv] [opcional: noreplace]

import sys, csv, webbrowser, bs4, requests, re, shutil, datetime
from collections import OrderedDict

# Desativa a exigência de certificado HTTPS ao pegar as informações
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Usa o arquivo determinado pelo primeiro argumento como fonte dos sites e nomes
csvFile = sys.argv[1]
noReplace = False
if len(sys.argv) > 2:
    if sys.argv[2] == "noreplace":
        noReplace = True

# Popula um dicionário com as informações do CSV
startupList = []
with open(csvFile, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)
    fh.close()

# Adiciona as informações coletadas como colunas caso elas já não existam
scraperKeys = ['Nome', 'Site', 'CNPJ', 'LinkedIn', 'Facebook', 'Instagram', 'Twitter', 'Crunchbase']
for key in scraperKeys:
    if key not in startupList[0]:
        startupList[0][key] = ""

# Cria um CSV com as colunas relevantes para servir de output
all_keys = startupList[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()

# Requisita o site da startup e faz download dele usando o Requests
def getSite(site):
    if ("http" and "://") not in site:
        site = "http://" + site
    try:
        res = requests.get(site, verify=False)
    except Exception as e:
        return 'ERRO', e
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    return soup, res.status_code

# Busca números no formato de CNPJ no site e retorna os resultados
def scrapeCnpj(content):
    cnpjRegex = re.compile(r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}")
    results = cnpjRegex.findall(content.text)
    return results

# Busca links na página contendo "termos" ou "terms" e retorna uma lista deles
def getTermos(content):
    termosRegex = re.compile(".*(Termos|Terms).*", re.IGNORECASE)
    termosResults = content.find_all("a", href=True, title=termosRegex)
    results = []
    for item in termosResults:
        site, response = getSite(item['href'])
        if response != 200:
            continue
        result = scrapeCnpj(site)
        results += result
    return results

# Busca links na página contendo "privacidade" ou "privacy" e retorna uma lista deles
def getPrivacidade(content):
    privacidadeRegex = re.compile(".*(Privacidade|Privacy).*", re.IGNORECASE)
    privacidadeResults = content.find_all("a", href=True, title=privacidadeRegex)
    results = []
    for item in privacidadeResults:
        site, response = getSite(item['href'])
        if response != 200:
            continue
        result = scrapeCnpj(site)
        results += result
    return results
    
# Roda o scrapeCnpj() no site principal, página de termos e página de política de privacidade, retorna lista com todos os resultados
def getCnpj(content):
    result = []
    mainScrape = scrapeCnpj(content)
    termosScrape = getTermos(content)
    privacidadeScrape = getPrivacidade(content)
    result = mainScrape + termosScrape + privacidadeScrape
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = "null"
        print("Nenhum CNPJ encontrado.")
    elif len(result) == 1:
        print("Um CNPJ encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um CNPJ encontrado: " + str(result))
    return result

# Busca links para páginas de empresa no LinkedIn e retorna os resultados
def getLinkedin(content):
    lkdRegex = re.compile(r"linkedin\.com\/company\/[^&?]*", re.IGNORECASE)
    soupResults = content.find_all("a", href=lkdRegex)
    result = []
    for item in soupResults:
        mo = lkdRegex.search(item['href'])
        result.append("http://" + mo.group().split("?", 1)[0].split("&", 1)[0].replace('/about',"").strip('/').lower()) 
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = "null"
        print("Nenhum LinkedIn encontrado.")
    elif len(result) == 1:
        print("Um LinkedIn encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um LinkedIn encontrado: " + str(result))
    return result

# Busca links para o Facebook e retorna os resultados
def getFacebook(content):
    fbRegex = re.compile(r"facebook\.com\/(pg\/|page\/|pages\/)?[^\/?&\.]*", re.IGNORECASE)
    soupResults = content.find_all('a', href=fbRegex)
    result = []
    for item in soupResults:
        mo = fbRegex.search(item['href'])
        url = ("http://" + mo.group().replace('/pages','').replace('/pg', '').replace('/profile', '').strip('/').lower())
        if url != "http://facebook.com":
            result.append(url)
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = "null"
        print("Nenhum Facebook encontrado.")
    elif len(result) == 1:
        print("Um Facebook encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Facebook encontrado: " + str(result))
    return result

# Busca links para o Instagram e retorna os resultados
def getInstagram(content):
    igRegex = re.compile(r"instagram\.com\/[^&?].*", re.IGNORECASE)
    soupResults = content.find_all("a", href=igRegex)
    result = []
    for item in soupResults:
        mo = igRegex.search(item['href'])
        result.append("http://" + mo.group().replace('/about',"").strip('/').lower())
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = "null"
        print("Nenhum Instagram encontrado.")
    elif len(result) == 1:
        print("Um Instagram encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Instagram encontrado: " + str(result))
    return result

# Busca links para o Twitter e retorna os resultados
def getTwitter(content):
    ttRegex = re.compile(r"twitter\.com\/[^&?].*", re.IGNORECASE)
    soupResults = content.find_all("a", href=ttRegex)
    result = []
    for item in soupResults:
        mo = ttRegex.search(item['href'])
        result.append("http://" + mo.group().replace('/about',"").strip('/').lower())
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = "null"
        print("Nenhum Twitter encontrado.")
    elif len(result) == 1:
        print("Um Twitter encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Twitter encontrado: " + str(result))
    return result

# Busca links para páginas de organização do Crunchbase e retorna os resultados
def getCrunchbase(content):
    cbRegex = re.compile(r"crunchbase\.com\/organization\/.*$", re.IGNORECASE)
    soupResults = content.find_all("a", href=cbRegex)
    result = []
    for item in soupResults:
        mo = cbRegex.search(item['href'])
        result.append("http://" + mo.group().split("?", 1)[0].split("&", 1)[0].strip('/').lower())
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = "null"
        print("Nenhum Crunchbase encontrado.")
    elif len(result) == 1:
        print("Um Crunchbase encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Crunchbase encontrado: " + str(result))
    return result

# Pega o site de cada startup do CSV e roda cada uma das buscas as buscas nele
for startup in startupList:
    print("(" + str(startupList.index(startup) + 1) + "/" + str(len(startupList)) + ")" + "\nRequisitando site da " + startup['Nome'] + "...")
    print("URL: " + startup['Site'])
    site, response = getSite(startup['Site'])
    startup['Response'] = response
    if response != 200:
        print("SITE RETORNOU ERRO. Código retornado: " + str(response))
        print("\n")
        outputWriter.writerow(startup)
        continue
    if noReplace == False:
        startup['CNPJ'] = getCnpj(site)
        startup['LinkedIn'] = getLinkedin(site)
        startup['Facebook'] = getFacebook(site)
        startup['Twitter'] = getTwitter(site)
        startup['Instagram'] = getInstagram(site)
        startup['Crunchbase'] = getCrunchbase(site)
    elif noReplace == True:
        if ('CNPJ' not in startup) or (startup['CNPJ'] == ''):
            startup['CNPJ'] = getCnpj(site)
        if 'LinkedIn' not in startup or startup['LinkedIn'] == '':
            startup['LinkedIn'] = getLinkedin(site)
        if 'Facebook' not in startup or startup['Facebook'] == '':
            startup['Facebook'] = getFacebook(site)
        if 'Twitter' not in startup or startup['Twitter'] == '':
            startup['Twitter'] = getTwitter(site)
        if 'Instagram' not in startup or startup['Instagram'] == '':
            startup['Instagram'] = getInstagram(site)
        if 'Crunchbase' not in startup or startup['Crunchbase'] == '':
            startup['Crunchbase'] = getCrunchbase(site)
    outputWriter.writerow(startup)
    print("\n")

# Fecha o arquivo de output, renomeia para evitar substituição e finaliza o programa
outputFile.close()
now = datetime.datetime.now()
shutil.move("output.csv", "output " + now.strftime("%Y-%m-%d %Hh%Mm") + ".csv")
print("Tarefa concluída.")
sys.exit()