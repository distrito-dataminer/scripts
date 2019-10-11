#! python3
# cleaner.py - Limpa dados de um CSV para mantê-los no padrão Dataminer

import sys
import csv
import re
import pprint
from pycpfcnpj import cnpj as pycnpj
from datetime import datetime, timedelta
from more_itertools import unique_everseen as unique
from collections import OrderedDict
from unidecode import unidecode
from utils import datasets
import itertools

def clean(startupList):

    invalidCnpjs = []

    for startup in startupList:

        # Limpa o CNPJ, adicionando 0s que o Excel come e tirando símbolos
        if 'CNPJ' in startup:
            if startup['CNPJ']:
                cnpjList = startup['CNPJ'].strip().split(',')
                while '' in cnpjList:
                    cnpjList.remove('')
                newCnpjList = []
                for cnpj in cnpjList:
                    newCnpj = re.sub(r'[^\d]', '', cnpj)
                    newCnpj = newCnpj.zfill(14)
                    if newCnpj == '00000000000000':
                        continue
                    if pycnpj.validate(newCnpj):
                        newCnpj = "{}.{}.{}/{}-{}".format(
                            newCnpj[:2], newCnpj[2:5], newCnpj[5:8], newCnpj[8:12], newCnpj[12:14])
                        newCnpjList.append(newCnpj)
                    else:
                        invalidCnpjs.append(
                            startup['Startup'])
                while '' in newCnpjList:
                    newCnpjList.remove('')
                startup['CNPJ'] = ','.join(list(unique(newCnpjList)))

    # Limpa o site, mantendo formato consistente e letras minúsculas
        if 'Site' in startup:
            if startup['Site']:
                newSite = startup['Site'].lower().replace(
                    "https://", "http://")
                if "http://" not in newSite:
                    newSite = "http://" + newSite
                newSite = newSite.replace("www.", "")
                siteRegex = re.compile(r'http:\/\/[^\/&?"]*', re.IGNORECASE)
                mo = siteRegex.search(newSite)
                if mo != None:
                    newSite = mo.group().lower().strip().strip('/').strip()
                if newSite in datasets.invalidsites:
                    print('Site inválido: {}. Removendo.'.format(startup['Site']))
                    startup['Site'] = ''
                else:
                    startup['Site'] = newSite
        
        if 'Site final' in startup:
            if startup['Site final']:
                newSite = startup['Site final'].lower().replace(
                    "https://", "http://")
                if "http://" not in newSite:
                    newSite = "http://" + newSite
                newSite = newSite.replace("www.", "")
                siteRegex = re.compile(r'http:\/\/[^\/&?"]*', re.IGNORECASE)
                mo = siteRegex.search(newSite)
                if mo != None:
                    newSite = mo.group().lower().strip().strip('/').strip()
                    startup['Site final'] = newSite

    # Limpa o URL do LinkedIn
        if 'LinkedIn' in startup:
            if startup['LinkedIn']:
                newLkdList = []
                lkdList = startup['LinkedIn'].strip().split(',')
                for lkd in lkdList:
                    lkdRegex = re.compile(
                        r'linkedin\.com\/company\/[^\/?"]*', re.IGNORECASE)
                    mo = lkdRegex.search(lkd)
                    if mo != None:
                        lkd = "http://" + mo.group().lower().strip()
                        if lkd in datasets.invalidLinkedin:
                            print('Removendo LKD inválido: {}'.format(lkd))
                        else:
                            newLkdList.append(lkd)
                    else:
                        print('Removendo LKD inválido: {}'.format(lkd))
                startup['LinkedIn'] = ','.join(list(unique(newLkdList)))

    # Limpa o URL do LinkedIn pessoal
        if 'LinkedIn Pessoal' in startup:
            if startup['LinkedIn Pessoal']:
                newLkdList = []
                lkdList = startup['LinkedIn Pessoal'].strip().split(',')
                for lkd in lkdList:
                    lkdRegex = re.compile(
                        r'linkedin\.com\/in\/[^\/?"]*', re.IGNORECASE)
                    mo = lkdRegex.search(lkd)
                    if mo != None:
                        lkd = "http://" + mo.group().lower().strip()
                        newLkdList.append(lkd)
                    else:
                        print('Removendo LKD inválido: {}'.format(lkd))
                startup['LinkedIn Pessoal'] = ','.join(list(unique(newLkdList)))

    # Limpa o URL do Facebook
        if 'Facebook' in startup:
            if startup['Facebook']:
                fbList = startup['Facebook'].strip().split(',')
                newFbList = []
                for fb in fbList:
                    fbRegex = re.compile(
                        r'facebook\.com\/(pg\/|page\/|pages\/)?[^\/&?\s"]*', re.IGNORECASE)
                    mo = fbRegex.search(fb)
                    if mo:
                        fb = "http://" + mo.group().lower().strip()
                        if fb not in datasets.invalidFacebook:
                            newFbList.append(fb)
                    else:
                        print("Removendo Facebook inválido: {}".format(fb))
                startup['Facebook'] = ','.join(list(unique(newFbList)))

    # Limpa o URL do Twitter
        if 'Twitter' in startup:
            if startup['Twitter']:
                ttList = startup['Twitter'].strip().split(',')
                newTtList = []
                for tt in ttList:
                    ttRegex = re.compile(
                        r'twitter\.com\/[^\/&?"]*', re.IGNORECASE)
                    mo = ttRegex.search(tt)
                    if mo != None:
                        tt = "http://" + mo.group().lower().strip()
                        if tt not in datasets.invalidTwitter:
                            newTtList.append(tt)
                    else:
                        if 'facebook' in tt.lower():
                            startup['Facebook'] += ',' + tt
                        elif 'linkedin' in tt.lower():
                            startup['LinkedIn'] += ',' + tt
                startup['Twitter'] = ','.join(list(unique(newTtList)))

    # Limpa o URL do Instagram
        if 'Instagram' in startup:
            if startup['Instagram']:
                instaList = startup['Instagram'].strip().split(',')
                newInstaList = []
                for insta in instaList:
                    instaRegex = re.compile(
                        r'instagram\.com\/[^\/&?"]*', re.IGNORECASE)
                    mo = instaRegex.search(insta)
                    if mo != None:
                        insta = "http://" + mo.group().lower().strip()
                        newInstaList.append(insta)
                    else:
                        print('Instagram inválido removido: {}'.format(insta))
                startup['Instagram'] = ','.join(list(unique(newInstaList)))

    # Limpa o URL do Crunchbase
        if 'Crunchbase' in startup:
            if (startup['Crunchbase']):
                cbList = startup['Crunchbase'].strip().split(',')
                newCbList = []
                for cb in cbList:
                    cbRegex = re.compile(
                        r'crunchbase\.com\/organization\/[^\/&?"]*', re.IGNORECASE)
                    mo = cbRegex.search(cb)
                    if mo != None:
                        cb = "http://" + mo.group().lower().strip()
                        newCbList.append(cb)
                    else:
                        print("Crunchbase inválido removido: {}".format(cb))
                startup['Crunchbase'] = ','.join(list(unique(cbList)))

    # Transforma o Estado em sigla
        if 'Estado' in startup:
            if startup['Estado']:
                estadoList = startup['Estado'].strip().split(',')
                newEstadoList = []
                for estado in estadoList:
                    if re.sub(r'[^\w]|\s', '', unidecode(estado.lower())) in datasets.siglas.keys() and estado not in datasets.siglas.values():
                        oldestado = estado
                        estado = datasets.siglas[re.sub(
                            r'[^\w]|\s', '', unidecode(estado.lower()))]
                        print('Alterando estado de {} para {}'.format(
                            oldestado, estado))
                    newEstadoList.append(estado)
                newEstadoList = list(unique(newEstadoList))
                while '' in newEstadoList:
                    newEstadoList.remove('')
                startup['Estado'] = ','.join(list(unique(newEstadoList)))

        if 'Cidade' in startup:
            if startup['Cidade']:
                cidadeList = startup['Cidade'].strip().split(',')
                newCidadeList = []
                for cidade in cidadeList:
                    if (cidade.upper().replace(' ', '') in datasets.siglas.values()) and (len(cidadeList) > 1):
                        print(
                            '{} é um estado e está como cidade. Removendo!'.format(cidade))
                        continue
                    if re.sub(r'[^\w]|\s', '', unidecode(cidade.lower())) in datasets.cidades.keys() and cidade not in datasets.cidades.values():
                        oldcidade = cidade
                        cidade = datasets.cidades[re.sub(
                            r'[^\w]|\s', '', unidecode(cidade.lower()))]
                        print('Alterando cidade de {} para {}'.format(
                            oldcidade, cidade))
                    newCidadeList.append(cidade)
                newCidadeList = list(unique(newCidadeList))
                while '' in newCidadeList:
                    newCidadeList.remove('')
                startup['Cidade'] = ','.join(list(unique(newCidadeList)))

        if 'Tags' in startup:
            if startup['Tags']:
                tagList = startup['Tags'].strip().split(',')
                newTagList = []
                for tag in tagList:
                    tag = tag.strip().replace("['", '').replace("']", '')
                    newTagList.append(tag)
                while '' in newTagList:
                    newTagList.remove('')
                startup['Tags'] = ','.join(list(unique(newTagList)))

        if 'Data de abertura' in startup:
            if startup['Data de abertura']:
                if '/Date(' in startup['Data de abertura']:
                    jsondate = startup['Data de abertura'][6:-7]
                    jsondate = int(jsondate)
                    jsondate = jsondate // 1000
                    if jsondate < 0:
                        mydate = datetime(1970, 1, 1) + \
                            timedelta(seconds=jsondate)
                    else:
                        mydate = datetime.fromtimestamp(jsondate)
                    startup['Data de abertura'] = mydate.strftime('%Y-%m-%d')

        if 'E-mail' in startup:
            if startup['E-mail']:
                emailList = startup['E-mail'].split(',')
                for email in emailList:
                    for invalidEmail in datasets.invalidEmail:
                        if invalidEmail in email:
                            emailList.remove(email)
                    charList = [' ', '[', ']', "'"]
                    for char in charList:
                        email = email.replace(char, '')
                    old_email = email
                    email = re.sub(r'(\(\d\d\))?\d+-\d+', '', email)
                    if email != old_email:
                        print('Changed {} to {}'.format(old_email, email))
                        emailList.remove(old_email)
                startup['E-mail'] = ','.join(list(unique(emailList)))

        if 'Descrição' in startup:
            if startup['Descrição']:
                while startup['Descrição'] != startup['Descrição'].strip().strip('\n'):
                    startup['Descrição'] = startup['Descrição'].strip().strip('\n')

    # Tira newlines e substitui por vírgulas pra separar mais de um item por célula
        exceptionList = ['Descrição']
        for key in startup:
            if key not in exceptionList:
                startup[key] = str(startup[key]).replace("\n", ",")

    if len(invalidCnpjs) > 0:
        print("CNPJs inválidos detectados - IDs e nomes:")
        print(*invalidCnpjs, sep='\n')
    return startupList


def score(startupList):
    for startup in startupList:
        score = 0
        if startup['Startup'] and startup['Site'] and startup['Fonte']:
            score += 5
        if startup['CNPJ']:
            score += 5
        if startup['Response']:
            score += 1
        if startup['LinkedIn']:
            score += 3
        if startup['Logo LKD']:
            score += 3
        if startup['Descrição']:
            score += 3
        if startup['Ano de fundação']:
            score += 3
        if startup['Cidade'] and startup['Estado'] and startup['País']:
            score += 3
        if startup['Funcionários LKD']:
            score += 3
        if startup['Faixa # de funcionários']:
            score += 1
        if startup['Setor']:
            score += 5
        if startup['Categoria']:
            score += 5
        if startup['Público']:
            score += 3
        if startup['Tags']:
            taglist = startup['Tags'].split(',')
            if len(taglist) >= 5:
                score += 2
            elif len(taglist) >= 10:
                score += 3
            elif len(taglist) >= 15:
                score += 4
        if startup['Crunchbase']:
            score += 2
        if startup['Facebook']:
            score += 1
        if startup['Instagram']:
            score += 1
        if startup['Twitter']:
            score += 1
        if startup['Faturamento Presumido']:
            score += 4
        # TODO: Outros dados TU - Score 2
        if 'E-mail' in startup and startup['E-mail']:
            score += 2
        if startup['Telefone'] and startup['Endereço']:
            score += 1
        if startup['Founders']:
            score += 2
        if startup['Modelo de negócio']:
            score += 3
        if 'Logo' in startup and startup['Logo'] == 'TRUE':
            score += 4
        if startup['Acelerada por'] or startup['Investida por'] or startup['Incubada por'] or startup['Hub de inovação']:
            score += 5
        if startup['CAC'] or startup['LTV'] or startup['Ticket Médio'] or startup['Churn Rate']                               \
                or startup['MRR'] or startup['GMV'] or startup['Visitantes no site por mês'] or startup['Taxa de Conversão']  \
                or startup['Downloads do App'] or startup['Usuários ativos'] or startup['Crescimento Receita Trimestral']     \
                or startup['Receita mensal atual'] or startup['Despesa mensal atual']:
            score += 5
        startup['NDP'] = round((score / 80) * 100)
    return startupList


def clean_endereco(enderecolist):

    for endereco in enderecolist:
        if len(endereco['CEP']) == 8:
            endereco['CEP'] = endereco['CEP'][0:5] + '-' + endereco['CEP'][5:]

    for index, endereco in enumerate(enderecolist):
        for index2, endereco2 in enumerate(enderecolist):
            if index == index2:
                continue
            if (endereco['Startup'], endereco['CEP']) == (endereco2['Startup'], endereco2['CEP']):
                enderecolist.remove(endereco2)

    return enderecolist



def dedupe(startup_list, scoring=True):
    
    startup_list = clean(startup_list)
    if scoring:
        startup_list = score(startup_list)

    dupes_list = []
    lkd_dupe_list = []

    for startup in startup_list:
        dupe_list = [startup]
        startup['Dedupe check'] = True
        clean_name = unidecode(startup['Startup'].lower().replace(' ', ''))
        clean_site = startup['Site'].replace('http://', '')
        if 'Site final' in startup:
            clean_finalsite = startup['Site final'].replace('http://', '')
        for startup2 in startup_list:
            if 'Dedupe check' in startup2 and startup2['Dedupe check'] == True:
                continue
            clean_site2 = startup2['Site'].replace('http://', '')
            if clean_site != '' and clean_site2 != '':
                if clean_site == clean_site2:
                    print('Site match! {} and {}'.format(startup['Site'], startup2['Site']))
                    dupe_list.append(startup2)
                    continue
            if 'Site final' in startup and 'Site final' in startup2:
                clean_finalsite2 = startup2['Site final'].replace('http://', '')
                if clean_finalsite != '' and clean_finalsite2 != '':
                    if clean_finalsite == clean_finalsite2:
                        print('Final site match! {} and {}'.format(startup['Site final'], startup2['Site final']))
                        dupe_list.append(startup2)
                        continue
            clean_name2 = unidecode(startup2['Startup'].lower().replace(' ', ''))
            if clean_name != '' and clean_name2 != '':
                if clean_name == clean_name2:
                    print('Name match! {} and {}'.format(startup['Startup'], startup2['Startup']))
                    dupe_list.append(startup2)
                    continue
            if 'LinkedIn' in startup:
                if startup['LinkedIn'] and startup['LinkedIn'] == startup2['LinkedIn'] and not startup['Tirar?'] and not startup2['Tirar?']:
                    print('LinkedIn match! {} and {}'.format(startup['LinkedIn'], startup2['LinkedIn']))
                    lkd_dupe_list.append(startup2['LinkedIn'])
                    continue
        if len(dupe_list) > 1:
            dupes_list.append(dupe_list)

    for dupe_list in dupes_list:
        new_startup = {}
        all_tags = []
        all_setor = []
        all_cat = []
        all_sub = []
        all_email = []
        max_ndp = 0
        min_id = 0
        if scoring:
            for dupe in dupe_list:
                if dupe['NDP'] == '':
                    ndp = 1
                else:
                    ndp = int(dupe['NDP'])
                if ndp >= max_ndp:
                    main_startup = dupe
        else:
            for dupe in dupe_list:
                if min_id == 0 or int(dupe['ID']) < min_id:
                    main_startup = dupe
                    min_id = int(dupe['ID'])
        if 'Tirar?' in main_startup and main_startup['Tirar?']:
            print('Main startup is marked for removal: {}'.format(main_startup['Startup']))
            print('Reason: {}'.format(main_startup['Tirar?']))
            if main_startup['Tirar?'] == 'Duplicata':
                print('Como está marcada como Duplicata, será desmarcada e usada como entrada principal.')
                main_startup['Tirar?'] = ''
        for key in main_startup:
            new_startup[key] = main_startup[key]
        for dupe in dupe_list:
            for key in startup:
                if key == 'Tirar?':
                    if startup[key] and (startup[key] != 'Duplicata'):
                        new_startup[key] = dupe[key]
                elif dupe[key]:
                    if new_startup[key] == '' and dupe[key] != '':
                        new_startup[key] = dupe[key]
            if 'Descrição' in dupe and dupe['Descrição'] not in new_startup['Descrição']:
                new_startup['Descrição'] = '\n\n' + dupe['Descrição']
            if 'Tags' in dupe:
                all_tags += dupe['Tags'].split(',')
            if 'Setor' in dupe:
                all_setor += dupe['Setor'].split(',')
            if 'Categoria' in dupe:
                all_cat += dupe['Categoria'].split(',')
            if 'Subcategoria' in dupe: 
                all_sub += dupe['Subcategoria'].split(',')
            if 'E-mail' in dupe:
                all_email += dupe['E-mail'].split(',')
        new_startup['Tags'] = ','.join(list(unique(all_tags)))
        new_startup['Setor'] = ','.join(list(unique(all_setor)))
        new_startup['Categoria'] = ','.join(list(unique(all_cat)))
        new_startup['Subcategoria'] = ','.join(list(unique(all_sub)))
        new_startup['E-mail'] = ','.join(list(unique(all_email)))
        if 'Tirar?' in new_startup and new_startup['Tirar?'] == 'Duplicata':
            print('{} - {} estava marcada como duplicata mas agora é a entrada principal.'.format(new_startup['ID'], new_startup['Startup']))
            new_startup['Tirar?'] = ''
        for index, startup in enumerate(startup_list):
            if startup == main_startup:
                print('Substituindo startup principal!')
                startup_list[index] = new_startup
            else:
                if startup in dupe_list:
                    print('Marcando duplicata para remoção!')
                    startup_list[index]['Tirar?'] = 'Duplicata'

    print('LKD Dupes:')
    pprint.pprint(lkd_dupe_list)

    return startup_list



def strip_fields(startup_list):

    multi_fields = ['Tags', 'Setor', 'Público', 'Founders', 'E-mail', 'Categoria', 'Subcategoria']

    for startup in startup_list:
        for key in startup:
            if startup[key]:
                startup[key] = startup[key].strip()
                if key in multi_fields:
                    full_list = startup[key].split(',')
                    new_list = []
                    for item in full_list:
                        new_list.append(item.strip())
                    startup[key] = ','.join(new_list)

    return startup_list

def bare(name):
    bare_name = re.sub(r'[\W_]+', '', unidecode(name).lower().strip())
    return bare_name