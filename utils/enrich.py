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


def enrich(startupList):
    errorlist = []
    addressList = []
    for startup in startupList:
        try:
            if startup['CNPJ'] != '' and startup['Razão Social'] == '':
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