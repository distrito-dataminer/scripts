#! python3

import requests
import json
import re
import pprint
import geocoder
from utils import privatekeys
from collections import OrderedDict
from time import sleep
from more_itertools import unique_everseen as unique


devkey = privatekeys.devkey
token = privatekeys.tokenTU


def create_address(endereco, startup):
    address = OrderedDict([('Startup ID', ''), ('Startup', ''), ('CNPJ', ''), ('CEP', ''),
                           ('Estado', ''), ('Cidade', ''), ('Bairro', '',),
                           ('Logradouro', ''), ('Tipo da rua',
                                                ''), ('Nome da rua', ''),
                           ('Número', ''), ('Complemento', ''), ('End. Fiscal', '')])
    address['Startup ID'] = startup['ID']
    address['Startup'] = startup['Startup']
    address['CNPJ'] = startup['CNPJ']
    address['Complemento'] = endereco['DS_COMPLEMENTO']
    address['Bairro'] = endereco['NM_BAIRRO']
    address['Cidade'] = endereco['NM_CIDADE']
    address['Nome da rua'] = endereco['NM_LOGRADOURO']
    address['CEP'] = str(endereco['NR_CEP']).zfill(8)
    address['Número'] = str(endereco['NR_LOGRADOURO'])
    address['Estado'] = endereco['SG_ESTADO']
    if 'TP_LOGRADOURO' in endereco:
        address['Tipo da rua'] = endereco['TP_LOGRADOURO']
    address['End. Fiscal'] = str(endereco['FG_FISCAL'])
    address['Logradouro'] = (address['Tipo da rua'] + ' ' + address['Nome da rua'] +
                             ' ' + address['Número'] + ' ' + address['Complemento']).strip()
    return address

def create_address_from_startup(startup):
    address = OrderedDict([('Startup ID', ''), ('Startup', ''), ('CNPJ', ''), ('CEP', ''),
                           ('Estado', ''), ('Cidade', ''), ('Bairro', '',),
                           ('Logradouro', ''), ('Tipo da rua',
                                                ''), ('Nome da rua', ''),
                           ('Número', ''), ('Complemento', ''), ('End. Fiscal', '')])
    address['Startup ID'] = startup['ID']
    address['Startup'] = startup['Startup']
    address['CNPJ'] = startup['CNPJ']
    address['End. Fiscal'] = startup['Fonte']
    address['Logradouro'] = startup['Endereço']
    return address

def lkd_address(endereco, startup):
    address = OrderedDict([('Startup ID', ''), ('Startup', ''), ('CNPJ', ''), ('CEP', ''),
                           ('Estado', ''), ('Cidade', ''), ('Bairro', '',),
                           ('Logradouro', ''), ('Tipo da rua',
                                                ''), ('Nome da rua', ''),
                           ('Número', ''), ('Complemento', ''), ('End. Fiscal', '')])
    if 'Startup' in startup:
        address['Startup'] = startup['Startup']
    if 'ID' in startup:
        address['Startup ID'] = startup['ID']
    if 'CNPJ' in startup:
        address['CNPJ'] = startup['CNPJ']
    if 'headquarter' in endereco:
        if endereco['headquarter'] == True:
            address['End. Fiscal'] = 'HQ LKD'
    if 'city' in endereco:
        address['Cidade'] = endereco['city']
    if 'postalCode' in endereco:
        zipcode = re.sub(r'[^\d]', '', endereco['postalCode']).strip()
        if len(zipcode) == 8:
            address['CEP'] = zipcode
    if 'geographicArea' in endereco:
        address['Estado'] = endereco['geographicArea']
    keysArray = ['line1', 'line2']
    addlines = [endereco[x] for x in keysArray if x in endereco]
    meuEnd = ''
    for i in range(len(addlines)):
        meuEnd += ', ' + addlines[i]
    meuEnd = meuEnd.strip().strip(',').strip()
    address['Logradouro'] = meuEnd
    return address


def enrich(startupList, replace=False):
    errorlist = []
    addressList = []
    for startup in startupList:
        try:
            if startup['CNPJ']:
                if 'Razão Social' in startup and startup['Razão Social'] and replace == False:
                    continue
                print("Enriquecendo dados de " + startup['Startup'] + '...')
                cnpj = startup['CNPJ']
                cnpj = re.sub(r'[^\d]', '', cnpj)
                url = (r'https://service.zipcode.com.br/RestService.svc/ConsultaPJ/json?token=' +
                       token + r'&cnpj=' + cnpj)
                try:
                    data = requests.get(url).json()
                except Exception as e:
                    print('Erro ao conectar à API:')
                    print(repr(e))
                if 'ERRO' in data:
                    print('API retornou erro ao buscar a ' +
                          startup['Startup'])
                    print('Código: ' + str(data['ERRO']['CODIGO']))
                    print('Mensagem: ' + str(data['ERRO']['MENSAGEM']))
                    errorlist.append({'CNPJ': startup['CNPJ'], 'Startup': startup['Startup'], 'Erro': str(
                        data['ERRO']['MENSAGEM'])})
                    continue
                try:
                    perfil = data['PERFIL_EMPRESARIAL']
                    startup['Faturamento Presumido'] = perfil['FATURAMENTO_PRESUMIDO']
                    startup['Faixa # de funcionários'] = perfil['FAIXA_FUNCIONARIOS'].replace(
                        "De ", "").replace("a", "-")
                    startup['Probabilidade de funcionamento'] = perfil['PROBABILIDADE_FUNCIONAMENTO']
                except Exception as e:
                    print(startup['Startup'] +
                          " deu erro no perfil empresarial.")
                    print(repr(e))
                try:
                    emaillist = []
                    for email in data['EMAILS']:
                        emaillist.append(email['DS_EMAIL'])
                        if 'E-mail' in startup:
                            if startup['E-mail']:
                                currentEmails = startup['E-mail'].split(',')
                                emaillist = emaillist + currentEmails
                        emaillist = list(unique(emaillist))
                        startup['E-mail'] = ','.join(emaillist)
                except Exception as e:
                    print(startup['Startup'] + " deu erro no e-mail:")
                    print(repr(e))
                try:
                    dados = data['DADOS_PRINCIPAIS']
                    startup['Razão Social'] = dados['NM_RAZAO_SOCIAL']
                    startup['Data de abertura'] = dados['DT_ABERTURA']
                    startup['Porte'] = dados['DS_PORTE']
                except Exception as e:
                    print(startup['Startup'] +
                          " deu erro nos dados principais:")
                    print(repr(e))
                try:
                    startup['Segmento CNPJ'] = data['DADOS_COMPLEMENTARES']['DS_SEGMENTO']
                    startup['Natureza Jurídica'] = data['DADOS_COMPLEMENTARES']['DS_NATUREZAJURIDICA']
                except Exception as e:
                    print(startup['Startup'] +
                          " deu erro nos dados complementares:")
                    print(repr(e))
                try:
                    startup['Número de sócios'] = len(data['QSA_PJ'])
                except Exception as e:
                    print(startup['Startup'] +
                          " deu erro no número de sócios:")
                    print(repr(e))
                try:
                    socio_list = [str(socio['NR_CPF']) for socio in data['QSA_PJ'] if socio['NR_CPF'] != -1]
                    startup['CPFs Sócios'] = ','.join(socio_list)
                except Exception as e:
                    print(startup['Startup'] + " deu erro ao pegar o CPF dos sócios:")
                    print(repr(e))
                try:
                    enderecos = data['ENDERECOS']
                except Exception as e:
                    print('Erro ao obter os endereços.')
                    print(repr(e))
                try:
                    for endereco in enderecos:
                        addressList.append(create_address(endereco, startup))
                except Exception as e:
                    print('Erro ao adicionar endereço.')
                    print(repr(e))
        except:
            continue
    return startupList, errorlist, addressList


def get_address(startupList):
    addressList = []
    for startup in startupList:
        try:
            if startup['CNPJ']:
                print("Obtendo endereço de " + startup['Startup'] + '...')
                cnpj = startup['CNPJ']
                cnpj = re.sub(r'[^\d]', '', cnpj)
                url = (r'https://service.zipcode.com.br/RestService.svc/ConsultaPJ/json?token=' +
                       token + r'&cnpj=' + cnpj)
                try:
                    data = requests.get(url).json()
                except Exception as e:
                    print('Erro ao conectar à API:')
                    print(repr(e))
                try:
                    enderecos = data['ENDERECOS']
                except Exception as e:
                    print('Erro ao obter os endereços.')
                    print(repr(e))
                try:
                    for endereco in enderecos:
                        addressList.append(create_address(endereco, startup))
                except Exception as e:
                    print('Erro ao adicionar endereço.')
                    print(repr(e))
        except Exception as e:
            print("Erro ao obter dados da {}".format(startup['Startup']))
            print(repr(e))
    return addressList

    
def geocode(enderecoList):
    newAddressList = []
    for endereco in enderecoList:
        keyList = ['ID', 'Startup ID', 'Startup', 'CNPJ', 'End. Fiscal', 'Confiança', 'Endereço', 'País',
                   'Estado', 'Cidade', 'Bairro', 'Rua', 'Número', 'Latitude', 'Longitude', 'CEP', 'Endereço original']
        newAddress = {}
        for key in keyList:
            newAddress[key] = ''
        carryOver = ['Startup ID', 'Startup', 'CNPJ', 'End. Fiscal']
        for key in carryOver:
            newAddress[key] = endereco[key]
        newAddress['Endereço original'] = endereco['Logradouro']
        print('Obtendo geocode de endereço da ' + endereco['Startup'])
        if endereco['Logradouro']:
            try:
                g = geocoder.google(location=(endereco['Logradouro'] + ',' + endereco['Cidade'] +
                ',' + endereco['Estado'] + ',' + endereco['CEP']), key=devkey, timeout=10, rate_limit=False)
                newAddress['Latitude'] = g.lat
                newAddress['Longitude'] = g.lng
                newAddress['Confiança'] = g.confidence
                newAddress['País'] = g.country
                newAddress['Cidade'] = g.county 
                newAddress['Número'] = g.housenumber
                newAddress['Endereço'] = g.address
                newAddress['CEP'] = g.postal
                newAddress['Estado'] = g.state
                newAddress['Rua'] = g.street
                newAddress['Bairro'] = g.sublocality
                newAddressList.append(newAddress)
            except Exception as e:
                print(repr(e))
                continue
    return newAddressList

def geocode_individual(endereco):
    keyList = ['ID', 'Startup ID', 'Startup', 'CNPJ', 'End. Fiscal', 'Confiança', 'Endereço', 'País',
                   'Estado', 'Cidade', 'Bairro', 'Rua', 'Número', 'Latitude', 'Longitude', 'CEP', 'Endereço original']
    newAddress = {}
    for key in keyList:
        newAddress[key] = ''
    carryOver = ['Startup ID', 'Startup', 'CNPJ', 'End. Fiscal']
    for key in carryOver:
        newAddress[key] = endereco[key]
    newAddress['Endereço original'] = endereco['Logradouro']
    print('Obtendo geocode de endereço da ' + endereco['Startup'])
    if endereco['Logradouro']:
        try:
            g = geocoder.google(location=(endereco['Logradouro'] + ',' + endereco['Cidade'] +
            ',' + endereco['Estado'] + ',' + endereco['CEP']), key=devkey, timeout=10, rate_limit=False)
            newAddress['Latitude'] = g.lat
            newAddress['Longitude'] = g.lng
            newAddress['Confiança'] = g.confidence
            newAddress['País'] = g.country
            newAddress['Cidade'] = g.county 
            newAddress['Número'] = g.housenumber
            newAddress['Endereço'] = g.address
            newAddress['CEP'] = g.postal
            newAddress['Estado'] = g.state
            newAddress['Rua'] = g.street
            newAddress['Bairro'] = g.sublocality
            return newAddress
        except Exception as e:
            print(repr(e))
            return None



def info_from_address(base, enderecos):

    for startup in base:
        if startup['Cidade'] == '' or startup['Estado'] == '':
            for endereco in enderecos:
                if endereco['End. Fiscal'].lower() in ['', 'false']:
                    continue
                if endereco['Startup ID'] == startup['ID']:
                    if startup['Cidade'] == '' and endereco['Cidade'] != '':
                        print('{} não tinha cidade e agora tem!'.format(startup['Startup']))
                        startup['Cidade'] = endereco['Cidade']
                    if startup['Estado'] == '' and endereco['Estado'] != '':
                        print('{} não tinha estado e agora tem!'.format(startup['Startup']))
                        startup['Estado'] = endereco['Estado']
                    if startup['Endereço'] == '' and endereco['Logradouro'] != '':
                        print('{} não tinha endereço e agora tem!'.format(startup['Startup']))
                        startup['Endereço'] = endereco['Logradouro']

    for startup in base:
        if startup['Cidade'] == '' or startup['Estado'] == '':
            for endereco in enderecos:
                if endereco['Startup ID'] == startup['ID']:
                    if startup['Cidade'] == '' and endereco['Cidade'] != '':
                        print('{} não tinha cidade e agora tem!'.format(startup['Startup']))
                        startup['Cidade'] = endereco['Cidade']
                    if startup['Estado'] == '' and endereco['Estado'] != '':
                        print('{} não tinha estado e agora tem!'.format(startup['Startup']))
                        startup['Estado'] = endereco['Estado']
                    if startup['Endereço'] == '' and endereco['Logradouro'] != '':
                        print('{} não tinha endereço e agora tem!'.format(startup['Startup']))
                        startup['Endereço'] = endereco['Logradouro']

    return base



def serpapi_lkd(startup_list, no_replace=True, max_count=3500):

    from serpapi.google_search_results import GoogleSearchResults

    key = privatekeys.serpapi_key
    num_results = 1
    start = 0
    count = 0
    success_count = 0
    location = 'Brazil'

    if no_replace:
        print('Startups que já têm LinkedIn, já passaram pelo bot ou estão marcadas para remoção serão puladas!')

    for startup in startup_list:
        if no_replace and startup['LinkedIn']:
            #print('{} já tem LinkedIn.'.format(startup['Startup']))
            continue
        if 'Bot LinkedIn' in startup and startup['Bot LinkedIn']:
            print('{} já passou pelo bot do LinkedIn'.format(startup['Startup']))
            continue
        if startup['Tirar?']:
            print('{} está marcada para remoção.'.format(startup['Startup']))
            continue
        print('Pegando LinkedIn de {}'.format(startup['Startup']))
        count += 1
        if count >= max_count:
            break
        clean_site = startup['Site'].lower().replace('http://', '')
        query = 'site:www.linkedin.com/company "{}"'.format(clean_site)
        client = GoogleSearchResults({"q": query, "location": location, "api_key": key, "num": num_results, "start": start, "device": "desktop", "nfpr": 1, "filter": 1, "gl": "br"})
        search_result = client.get_dict()
        startup['Bot LinkedIn'] = 'TRUE'
        if 'organic_results' in search_result:
            if 'link' in search_result['organic_results'][0] and 'snippet' in search_result['organic_results'][0]:
                snippet = search_result['organic_results'][0]['snippet']
                if clean_site not in snippet:
                    print('Site não estava no snippet.')
                    continue
                lkd = search_result['organic_results'][0]['link']
                try:
                    lkdRegex = re.compile(
                        r'linkedin\.com\/company\/[^\/?"]*', re.IGNORECASE)
                    mo = lkdRegex.search(lkd)
                    if mo != None:
                        lkd = "http://" + mo.group().lower().strip()
                        startup['LinkedIn'] = lkd
                        success_count += 1
                        print(lkd)
                    else:
                        print('Link não bateu com regex: {}'.format(lkd))
                except Exception as e:
                    print(e)
            else:
                print('Resultado não tem link ou não tem snippet: {}'.format(search_result))
        else:
            print('Nenhum resultado encontrado.')

    print('De {} startups, {} tiveram LinkedIn encontrado.'.format(count, success_count))

    return startup_list