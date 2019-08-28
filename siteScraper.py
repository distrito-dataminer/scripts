#! python3
# siteScraper.py - encontra informações relevantes de startups em sites contidos em um csv
# Informações coletadas: CNPJ, LinkedIn, Facebook, Instagram, Twitter, Crunchbase
# O csv deve conter pelo menos as colunas 'Startup' e 'Site'.
# Uso: python cnpjScraper.py [csv] [opcional: noreplace]

import sys, csv, webbrowser, bs4, requests, re, shutil, datetime
from collections import OrderedDict
from utils import cleaner, ddmdata, sanity
from more_itertools import unique_everseen as unique

# Desativa a exigência de certificado HTTPS ao pegar as informações
import urllib3
urllib3.disable_warnings()

# Usa o arquivo determinado pelo primeiro argumento como fonte dos sites e nomes
csvFile = sys.argv[1]
noReplace = False
if len(sys.argv) > 2:
    if sys.argv[2] == "noreplace":
        noReplace = True

min = 0
max = 999999

if len(sys.argv) > 3:
    min = sys.argv[3]
    max = sys.argv[4]

# Popula um dicionário com as informações do CSV
startupList = ddmdata.readcsv(sys.argv[1])

# Adiciona as informações coletadas como colunas caso elas já não existam
scraperKeys = ['ID', 'Startup', 'Site', 'CNPJ', 'LinkedIn', 'Facebook', 'Instagram', 'Twitter', 'Crunchbase', 'Response', 'E-mail']
for key in scraperKeys:
    for startup in startupList:
        if key not in startup:
            startup[key] = ""

# Cria um CSV com as colunas relevantes para servir de output
all_keys = startupList[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'If-Modified-Since': 'Mon, 08 Jul 2019 18:10:47 GMT',
    'If-None-Match': '5f879487d25a59f2e5f968f7b6bd5799',
    'Cache-Control': 'max-age=0',
}

# Requisita o site da startup e faz download dele usando o Requests
def getSite(site):
    if ("http" and "://") not in site:
        site = "http://" + site
    try:
        res = requests.get(site, verify=False, timeout=(2, 15), headers=headers)
    except Exception as e:
        try:
            print('Erro. Adicionando WWW.')
            site = site.replace('http://', 'http://www.')
            res = requests.get(site, verify=False, timeout=(2, 15))
        except:
            print('Erro mesmo com WWW. Enviando erro original.')
            return 'ERRO', repr(e)
    if res.status_code != 200:
        try:
            if 'http://www.' not in site:
                print('Status code ruim. Adicionando WWW.')
                site = site.replace('http://', 'http://www.')
                res2 = requests.get(site, verify=False, timeout=(2, 15))
                if res2.status_code == 200:
                    soup = bs4.BeautifulSoup(res2.text, features="lxml")
                    return soup, res2.status_code
                else:
                    print('Adicionar o WWW não resolveu. Prosseguindo com status code original.')
        except:
            print('Erro ao adicionar WWW. Prosseguindo com status code ruim.')
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    return soup, res.status_code

# Busca números no formato de CNPJ no site e retorna os resultados
def scrapeCnpj(content):
    cnpjRegex = re.compile(r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}")
    results = cnpjRegex.findall(content.text)
    for item in results:
        mo = cnpjRegex.search(item)
        item = mo.group()
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
        print("Nenhum CNPJ encontrado.")
        return ''
    elif len(result) == 1:
        print("Um CNPJ encontrado: " + result[0])
        return result[0]
    elif len(result) > 1:
        print("Mais de um CNPJ encontrado: " + str(result))
        return ','.join(result)

# TODO: buscar CNPJ no registro do site no registro.br
def getRegistro(url):
    url = url.strip('/').replace('http://', '')
    if url[-3:] == ".br":
        print("CNPJ pode estar no registro do domínio! Verificar WHOIS.")
        return ""
    else:
        return ""

def getLogo(content):
    logoRegex = re.compile(r"""(https?:\/\/.[^"\s]*?logo.[^"\s]*?\.(png|jpg|svg|tif|jpeg|bmp))""", re.IGNORECASE)
    matches = re.findall(logoRegex, str(content))
    results = []
    for item in matches:
        results.append(item[0])
    if results == []:
        result = ""
        print("Nenhum Logo encontrado.")
    elif len(results) == 1:
        print("Um Logo encontrado: " + results[0])
        result = results[0]
    elif len(results) > 1:
        print("Mais de um Logo encontrado: " + str(results))
        result = results
    return result

# Busca links para páginas de empresa no LinkedIn e retorna os resultados
def getLinkedin(content):
    lkdRegex = re.compile(r"linkedin\.com\/company\/[^&?\/]*", re.IGNORECASE)
    soupResults = content.find_all("a", href=lkdRegex)
    result = []
    for item in soupResults:
        mo = lkdRegex.search(item['href'])
        result.append("http://" + mo.group().split("?", 1)[0].split("&", 1)[0].replace('/about',"").strip('/').lower()) 
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = ""
        print("Nenhum LinkedIn encontrado.")
    elif len(result) == 1:
        print("Um LinkedIn encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um LinkedIn encontrado: " + str(result))
    return result

# Busca links para o Facebook e retorna os resultados
def getFacebook(content):
    fbRegex = re.compile(r"(facebook|fb)\.com\/(pg\/|page\/|pages\/)?[^\/?&\.]*", re.IGNORECASE)
    soupResults = content.find_all('a', href=fbRegex)
    result = []
    for item in soupResults:
        mo = fbRegex.search(item['href'])
        url = ("http://" + mo.group().replace('/pages','').replace('/pg', '').replace('/profile', '').replace('fb.com', 'facebook.com').strip('/').lower())
        if url != "http://facebook.com":
            result.append(url)
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = ""
        print("Nenhum Facebook encontrado.")
    elif len(result) == 1:
        print("Um Facebook encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Facebook encontrado: " + str(result))
    return result

# Busca links para o Instagram e retorna os resultados
def getInstagram(content):
    igRegex = re.compile(r"instagram\.com\/[^&?\/]*", re.IGNORECASE)
    soupResults = content.find_all("a", href=igRegex)
    result = []
    for item in soupResults:
        mo = igRegex.search(item['href'])
        result.append("http://" + mo.group().replace('/about',"").strip('/').lower())
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = ""
        print("Nenhum Instagram encontrado.")
    elif len(result) == 1:
        print("Um Instagram encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Instagram encontrado: " + str(result))
    return result

# Busca links para o Twitter e retorna os resultados
def getTwitter(content):
    ttRegex = re.compile(r"twitter\.com\/[^&?\/]*", re.IGNORECASE)
    soupResults = content.find_all("a", href=ttRegex)
    result = []
    for item in soupResults:
        mo = ttRegex.search(item['href'])
        result.append("http://" + mo.group().replace('/about',"").strip('/').lower())
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = ""
        print("Nenhum Twitter encontrado.")
    elif len(result) == 1:
        print("Um Twitter encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Twitter encontrado: " + str(result))
    return result

# Busca links para páginas de organização do Crunchbase e retorna os resultados
def getCrunchbase(content):
    cbRegex = re.compile(r"crunchbase\.com\/organization\/[^&?\/]*", re.IGNORECASE)
    soupResults = content.find_all("a", href=cbRegex)
    result = []
    for item in soupResults:
        mo = cbRegex.search(item['href'])
        result.append("http://" + mo.group().split("?", 1)[0].split("&", 1)[0].strip('/').lower())
    result = list(OrderedDict.fromkeys(result))
    if result == []:
        result = ""
        print("Nenhum Crunchbase encontrado.")
    elif len(result) == 1:
        print("Um Crunchbase encontrado: " + result[0])
        result = result[0]
    elif len(result) > 1:
        print("Mais de um Crunchbase encontrado: " + str(result))
    return result

def scrapeEmail(content):
    emailRegex = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    results = emailRegex.findall(content.text)
    for item in results:
        mo = emailRegex.search(item)
        item = mo.group()
    return results

def getContato(content):
    contatoRegex = re.compile(".*(Contato|Contact|Fale Conosco).*", re.IGNORECASE)
    termosResults = content.find_all("a", href=True, title=contatoRegex)
    results = []
    for item in termosResults:
        site, response = getSite(item['href'])
        if response != 200:
            continue
        result = scrapeEmail(site)
        results += result
    return results

def getEmail(content, currentemails):
    result = []
    mainScrape = scrapeEmail(content)
    contatoScrape = getContato(content)
    result += mainScrape + contatoScrape
    result = list(unique(result))
    if result == []:
        print("Nenhum E-mail encontrado.")
    elif len(result) == 1:
        print("Um E-mail encontrado: " + result[0])
    elif len(result) > 1:
        print("Mais de um E-mail encontrado: " + str(result))
    if currentemails != '':
        currentemailslist = currentemails.split(',')
        result = result + currentemailslist
        result = list(unique(result))
    return ','.join(result)

# Pega o site de cada startup do CSV e roda cada uma das buscas as buscas nele
for startup in startupList:
    if startup['ID']:
        if int(startup['ID']) < int(min):
            outputWriter.writerow(startup)
            continue 
        if int(startup['ID']) > int(max):
            outputWriter.writerow(startup)
            continue
    # Comente esse trecho para reobter dados de startups que já tem o campo Response preenchido
    #if startup['Response'] != '':
    #    outputWriter.writerow(startup)
    #    print('\n{} já tem Response. Pulando para o próximo site... \n'.format(startup['Startup']))
    #    continue
    if 'Tirar?' in startup and startup['Tirar?']:
        outputWriter.writerow(startup)
        print('\n{} está marcada para remoção. Pulando para o próximo site... \n'.format(startup['Startup']))
        continue
    print("(" + str(startupList.index(startup) + 1) + "/" + str(len(startupList)) + ")" + "\nRequisitando site da " + startup['Startup'] + "...")
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
        if startup['CNPJ'] == "":
            startup['CNPJ'] = getRegistro(startup['Site'])
        startup['LinkedIn'] = getLinkedin(site)
        startup['Facebook'] = getFacebook(site)
        startup['Twitter'] = getTwitter(site)
        startup['Instagram'] = getInstagram(site)
        startup['Crunchbase'] = getCrunchbase(site)
        startup['E-mail'] = getEmail(site, startup['E-mail'])
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
        #if 'E-mail' not in startup or startup['E-mail'] == '':
        startup['E-mail'] = getEmail(site, startup['E-mail'])
    outputWriter.writerow(startup)
    print("\n")

# Fecha o arquivo de output, renomeia para evitar substituição e finaliza o programa
outputFile.close()
now = datetime.datetime.now()
shutil.move("output.csv", "siteScraper_output_" + now.strftime("%Y-%m-%d %Hh%Mm") + ".csv")
print("Tarefa concluída.")
sys.exit()