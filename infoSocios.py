#! python3
# infoSocios.py - Traz informações dos sócios de empresas a partir de um CSV de CNPJs

import sys
import csv
import re
import requests
import pprint
from collections import OrderedDict
from unidecode import unidecode
from utils import cleaner, enrich, ddmdata
from utils import privatekeys

# Define o dicionário de sócio e cria lista de sócios
socios = []

# Popula um dicionário com as informações do CSV
startupList = ddmdata.readcsv(sys.argv[1])

# Limpa os dados da lista de startups antes de trabalhar com eles
startupList = cleaner.clean(startupList)

def createSocio():
    socio = OrderedDict()
    socio['CPF'] = ''
    socio['Nome'] = ''
    socio['Cargo'] = ''
    socio['Empresa'] = ''
    socio['CNPJ'] = ''
    socio['Data de Nascimento'] = ''
    socio['Idade'] = ''
    socio['Sexo'] = ''
    socio['Cidade'] = ''
    socio['Estado'] = ''
    socio['Escolaridade'] = ''
    socio['Número de Empresas'] = ''
    return socio


# Cria lista de startups com erro no CNPJ
errorlist = []

# Faz uma busca em cada startup e obtém os dados de cada um dos seus sócios
for startup in startupList:
    if startup['CNPJ']:
        print("Buscando sócios da " + startup['Startup'] + '...')
        cnpj = startup['CNPJ']
        cnpj = re.sub(r'[^\d]', '', cnpj)
        url = (r'https://service.zipcode.com.br/RestService.svc/ConsultaPJ/json?token=' +
               privatekeys.tokenTU + r'&cnpj=' + cnpj)
        try:
            pj = requests.get(url, timeout=10).json()
        except Exception as e:
            print("Erro ao conectar à API Pessoa Jurídica:")
            print(repr(e))
            continue
        if 'ERRO' in pj:
            print('API retornou erro ao buscar a ' + startup['Startup'])
            print('Código: ' + str(pj['ERRO']['CODIGO']))
            print('Mensagem: ' + str(pj['ERRO']['MENSAGEM']))
            errorlist.append({'CNPJ': startup['CNPJ'], 'Startup': startup['Startup'], 'Erro': str(
                pj['ERRO']['MENSAGEM'])})
            continue
        try:
            qsa = pj['QSA_PJ']
        except:
            print("Não foi possível encontrar quadro de sócios da " +
                  startup['Startup'])
            continue
        for s in qsa:
            socio = createSocio()
            try:
                cpf = str(s['NR_CPF'])
                if cpf != '-1':
                    cpfFormatado = cpf.zfill(11)
                    cpfFormatado = "{}.{}.{}-{}".format(
                        cpfFormatado[:3], cpfFormatado[3:6], cpfFormatado[6:9], cpfFormatado[9:11])
                else:
                    cpfFormatado = 'Inválido'
                socio['CPF'] = cpfFormatado
                socio['Nome'] = s['NM_COMPLETO']
                socio['Cargo'] = s['DS_QUALIFICACAO']
                socio['Empresa'] = startup['Startup']
                socio['CNPJ'] = startup['CNPJ']
                print('Fazendo consulta aos dados de ' + socio['Nome'] + '...')
                urlpf = (r'https://service.zipcode.com.br/RestService.svc/ConsultaPF/json?token=' +
                         privatekeys.tokenTU + r'&cpf=' + cpf)
                try:
                    pf = requests.get(urlpf, timeout=10).json()
                except Exception as e:
                    print("Erro ao conectar à API Pessoa Física:")
                    print(repr(e))
                    socios.append(socio)
                    continue
                if 'ERRO' in pf:
                    print('API retornou erro ao buscar dados de ' +
                          socio['Nome'])
                    print('Código: ' + str(pf['ERRO']['CODIGO']))
                    print('Mensagem: ' + str(pf['ERRO']['MENSAGEM']))
                    socios.append(socio)
                    continue
                try:
                    socio['Data de Nascimento'] = pf['DADOS_PRINCIPAIS']['DT_NASCIMENTO']
                    socio['Sexo'] = pf['DADOS_PRINCIPAIS']['DS_SEXO']
                    socio['Idade'] = pf['DADOS_PRINCIPAIS']['NR_IDADE']
                except Exception as e:
                    print("Erro ao pegar Dados Principais do sócio " +
                          socio['Nome'])
                    print(repr(e))
                try:
                    socio['Estado'] = pf['ENDERECOS'][0]['SG_ESTADO']
                    socio['Cidade'] = pf['ENDERECOS'][0]['NM_CIDADE']
                except Exception as e:
                    print('Erro ao pegar o Endereço do sócio ' +
                          socio['Nome'])
                    print(repr(e))
                try:
                    socio['Escolaridade'] = pf['DADOS_COMPLEMENTARES']['DS_ESCOLARIDADE']
                except Exception as e:
                    print('Erro ao pegar a Escolaridade do sócio ' +
                          socio['Nome'])
                    print(repr(e))
                try:
                    socio['Número de Empresas'] = len(pf['QSA'])
                except Exception as e:
                    print('Erro ao pegar o número de empresas do sócio ' +
                          socio['Nome'])
                    print(repr(e))
                socios.append(socio)
            except Exception as e:
                print('Erro ao pegar informações de um sócio da ' +
                      startup['Nome'])
                print(repr(e))
                continue

# Cria um CSV com as colunas relevantes para servir de output e escreve os dados limpos
all_keys = []
for item in socios:
    for key in item:
        if key not in all_keys:
            all_keys.append(key)
outputFile = open((sys.argv[1].replace('.csv', '') +
                   '_socios.csv'), 'w', newline='', encoding="utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()
outputWriter.writerows(socios)
outputFile.close()

all_error_keys = []
for item in errorlist:
    if key in item:
        if key not in all_error_keys:
            all_error_keys.append(key)
errorFile = open((sys.argv[1].replace(
    '.csv', '') + '_socios_errors.csv'), 'w', newline='', encoding="utf8")
errorWriter = csv.DictWriter(errorFile, all_error_keys, delimiter=',')
errorWriter.writeheader()
errorWriter.writerows(errorlist)
errorFile.close()

print('De {} startups, {} apresentaram erro e estão em {}'.format(len(startupList),
                                                                  len(errorlist), (sys.argv[1].replace('.csv', '') + '_socios_errors.csv')))
