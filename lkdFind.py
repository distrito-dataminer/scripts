#! python3
# lkdFind.py - Obtém URLs do Linkedin a partir de uma lista de sites por meio do Google Custom Search
# Uso - python lkdFind.py [csv] [modo: find|add] <- substitui informações já presentes no csv
# Exemplo: python lkdFind.py startups.csv replace

import sys, csv, shutil, datetime
from googleapiclient.discovery import build
from utils import ddmdata, privatekeys, cleaner

# Conecta na API do Google com a chave de API providenciada
service = build("customsearch", "v1", developerKey=privatekeys.devkey)

startup_csv, mode = sys.argv[1], sys.argv[2]
valid_modes = ['find', 'add']
if mode.lower() not in valid_modes:
    print('Invalid mode. Please use one of the following modes as the second argument: {}'.format(valid_modes))

startup_list = ddmdata.readcsv(startup_csv)

def lkd_find(startup_list, query='Site', altquery='Startup'):
    result_list = []
    for startup in startup_list:
        if 'LinkedIn' in startup and startup['LinkedIn'] != '':
            #print(startup['Startup'] + ' já tem LinkedIn. Pulando.')
            continue
        if 'LinkedIn' in startup and startup['LinkedIn'] == '':
            print('Buscando pelo {}: {}'.format(query, startup[query]))
            res = service.cse().list(
                q=startup[query].replace('http://', ''),
                cx='002626537913979718585:pkjl9_mtdpm',
                num = 1,
            ).execute()
            if 'items' not in res.keys():
                print('Não encontrado. Buscando por {}: {}'.format(altquery, startup[altquery]))
                res = service.cse().list(
                    q=startup[altquery],
                    cx='002626537913979718585:pkjl9_mtdpm',
                    num = 1,
                ).execute()
                if 'items' not in res.keys():
                    print('Não encontrado. Prosseguindo sem resultado.')
                    result = ''
                else:
                    result = res['items'][0]['link']
                    print('Encontrado. {}'.format(result))
            else:
                result = res['items'][0]['link']
                print('Encontrado. {}'.format(result))
            final_result = {'LinkedIn': result}
            result_list.append(final_result)
    return result_list

def lkd_add(startup_list, query='Site', altquery='Startup'):
    count = 0
    for startup in startup_list:
        if 'LinkedIn' in startup and startup['LinkedIn'] != '':
            #print(startup['Startup'] + ' já tem LinkedIn. Pulando.')
            startup['Verificar LKD'] = 'Não precisa'
            continue
        if 'LinkedIn' in startup and startup['LinkedIn'] == '':
            print('Buscando pelo {}: {}'.format(query, startup[query]))
            res = service.cse().list(
                q='"'+startup[query].replace('http://', '')+'"',
                cx='002626537913979718585:pkjl9_mtdpm',
                num = 1,
            ).execute()
            if 'items' not in res.keys():
                print('Não encontrado. Buscando por {}: {}'.format(altquery, startup[altquery]))
                res = service.cse().list(
                    q='"'+startup[altquery]+'"',
                    cx='002626537913979718585:pkjl9_mtdpm',
                    num = 1,
                ).execute()
                if 'items' not in res.keys():
                    print('Não encontrado. Prosseguindo sem resultado.')
                    result = ''
                else:
                    result = res['items'][0]['link']
                    count += 1
                    print('Encontrado. {}'.format(result))
            else:
                result = res['items'][0]['link']
                count += 1
                print('Encontrado. {}'.format(result))
            startup['LinkedIn'] = result
            startup['Verificar LKD'] = 'VERIFICAR LKD'
    print('Total de LinkedIns novos coletados: {}'.format(count))
    return startup_list

now = datetime.datetime.now()

if mode.lower() == 'find':
    lkd_results = lkd_find(startup_list)
    ddmdata.writecsv(lkd_results, 'lkdFIND_output_{}.csv'.format(now.strftime("%Y.%m.%d-%Hh%Mm")))
    print('Task complete.')
elif mode.lower() == 'add':
    startup_list = lkd_add(startup_list)
    ddmdata.writecsv(startup_list, 'lkdADD_output_{}.csv'.format(now.strftime("%Y.%m.%d-%Hh%Mm")))
    print('Task complete.')
