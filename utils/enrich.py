#! python3

import requests
import json
import re
import pprint


def enrich(startupList, token):
    for startup in startupList:
        if startup['CNPJ']:
            print("Enriquecendo a " + startup['Nome'] + '...')
            cnpj = startup['CNPJ']
            cnpj = re.sub(r'[^\d]', '', cnpj)
            url = (r'https://service.zipcode.com.br/RestService.svc/ConsultaPJ/json?token=' +
                   token + r'&cnpj=' + cnpj)
            data = requests.get(url).json()
            if 'ERRO' in data:
                print('API retornou erro ao buscar a ' + startup['Nome'])
                print('Código: ' + str(data['ERRO']['CODIGO']))
                print('Mensagem: ' + str(data['ERRO']['MENSAGEM']))
                continue
            try:
                perfil = data['PERFIL_EMPRESARIAL']
                startup['Faturamento Presumido'] = perfil['FATURAMENTO_PRESUMIDO']
                startup['Faixa # de funcionários'] = perfil['FAIXA_FUNCIONARIOS'].replace(
                    "De ", "").replace("a", "-")
                startup['Probabilidade de funcionamento'] = perfil['PROBABILIDADE_FUNCIONAMENTO']
            except:
                print(startup['Nome'] + " deu erro no perfil empresarial.")
            try:
                emaillist = []
                for email in data['EMAILS']:
                    emaillist.append(email['DS_EMAIL'])
                    startup['E-mail'] = emaillist
            except:
                print(startup['Nome'] + " deu erro no e-mail.")
            try:
                dados = data['DADOS_PRINCIPAIS']
                startup['Razão Social'] = dados['NM_RAZAO_SOCIAL']
                startup['Data de abertura'] = dados['DT_ABERTURA']
                startup['Porte'] = dados['DS_PORTE']
            except:
                print(startup['Nome'] + " deu erro nos dados principais.")
            try:
                startup['Segmento CNPJ'] = data['DADOS_COMPLEMENTARES']['DS_SEGMENTO']
                startup['Natureza Jurídica'] = data['DADOS_COMPLEMENTARES']['DS_NATUREZAJURIDICA']
            except:
                print(startup['Nome'] + " deu erro nos dados complementares.")
            try:
                startup['Número de sócios'] = len(data['QSA_PJ'])
            except:
                print(startup['Nome'] + " deu erro no número de sócios.")
    return startupList

def infosocios(startupList, token):
    sexo = {}
    idade = {}
    escolaridade = {}
    localidade = {}
    for startup in startupList:
        if startup['CNPJ']:
            cnpj = re.sub(r'[^\d]', '', cnpj)
            url = (r'https://service.zipcode.com.br/RestService.svc/ConsultaPJ/json?token=' +
                   token + r'&cnpj=' + cnpj)
            data = requests.get(url).json()
            if 'ERRO' in data:
                continue
            socios = data['QSA_PJ']
            for socio in socios:
                cpf = socio['NR_CPF']
                sociourl = (r'https://service.zipcode.com.br/RestService.svc/ConsultaPF/json?token=' +
                            token + r'&cpf=' + cpf)
                sociodata = requests.get(sociourl).json()
                sexosocio = sociodata['DADOS_PRINCIPAIS']['DS_SEXO']
                if sexosocio in sexo:
                    sexo[sexosocio] += 1
                else:
                    sexo[sexosocio] = 1
                idadesocio = sociodata['DADOS_PRINCIPAIS']['NR_IDADE']
                if idadesocio in idade:
                    idade[idadesocio] += 1
                else:
                    idade[idadesocio] = 1
                escolaridadesocio = sociodata['DADOS_COMPLEMENTARES']['DS_ESCOLARIDADE']
                if escolaridadesocio in escolaridade:
                    escolaridade[escolaridadesocio] += 1
                else:
                    escolaridade[escolaridadesocio] = 1
                localidadesocio = sociodata['ENDERECOS']['0']['SG_ESTADO']
                if localidadesocio in localidade:
                    localidade[localidadesocio] += 1
                else:
                    localidade[localidadesocio] = 1
