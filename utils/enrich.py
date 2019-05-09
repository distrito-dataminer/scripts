#! python3

import requests
import json
import re
import pprint


def enrich(startupList, token):
    errorlist = []
    for startup in startupList:
        if startup['CNPJ']:
            print("Enriquecendo dados de " + startup['Nome'] + '...')
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
                print('API retornou erro ao buscar a ' + startup['Nome'])
                print('Código: ' + str(data['ERRO']['CODIGO']))
                print('Mensagem: ' + str(data['ERRO']['MENSAGEM']))
                errorlist.append({'CNPJ': startup['CNPJ'], 'Nome': startup['Nome'], 'Erro': str(
                    data['ERRO']['MENSAGEM'])})
                continue
            try:
                perfil = data['PERFIL_EMPRESARIAL']
                startup['Faturamento Presumido'] = perfil['FATURAMENTO_PRESUMIDO']
                startup['Faixa # de funcionários'] = perfil['FAIXA_FUNCIONARIOS'].replace(
                    "De ", "").replace("a", "-")
                startup['Probabilidade de funcionamento'] = perfil['PROBABILIDADE_FUNCIONAMENTO']
            except Exception as e:
                print(startup['Nome'] + " deu erro no perfil empresarial.")
                print(repr(e))
            try:
                emaillist = []
                for email in data['EMAILS']:
                    emaillist.append(email['DS_EMAIL'])
                    startup['E-mail'] = emaillist
            except Exception as e:
                print(startup['Nome'] + " deu erro no e-mail:")
                print(repr(e))
            try:
                dados = data['DADOS_PRINCIPAIS']
                startup['Razão Social'] = dados['NM_RAZAO_SOCIAL']
                startup['Data de abertura'] = dados['DT_ABERTURA']
                startup['Porte'] = dados['DS_PORTE']
            except Exception as e:
                print(startup['Nome'] + " deu erro nos dados principais:")
                print(repr(e))
            try:
                startup['Segmento CNPJ'] = data['DADOS_COMPLEMENTARES']['DS_SEGMENTO']
                startup['Natureza Jurídica'] = data['DADOS_COMPLEMENTARES']['DS_NATUREZAJURIDICA']
            except Exception as e:
                print(startup['Nome'] + " deu erro nos dados complementares:")
                print(repr(e))
            try:
                startup['Número de sócios'] = len(data['QSA_PJ'])
            except Exception as e:
                print(startup['Nome'] + " deu erro no número de sócios:")
                print(repr(e))
    return startupList, errorlist
