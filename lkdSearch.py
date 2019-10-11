#! python3
# linkToLinkedin.py - Obtém URLs do Linkedin a partir de uma lista de sites por meio do Google Custom Search
# Uso - python linkToLinkedin.py [csv] [opcional: noreplace] <- não substitui informações já presentes no csv
# Exemplo: python linkToLinkedin.py startups.csv noreplace

import sys, csv, shutil, datetime
from googleapiclient.discovery import build
from utils import ddmdata, privatekeys, cleaner

tags = ['"EdTech" + "Brasil"', '"Startup" + "educação"', '"EdTech" + "Educação"']
output = []

# Conecta na API do Google com a chave de API providenciada
service = build("customsearch", "v1", developerKey=privatekeys.devkey)

# Faz uma busca com o site da startup como query no LinkedIn
for tag in tags:
    print("Getting LinkedIn results for " + tag + "...")
    end_search = False
    index = 1
    while end_search == False:
        try:
            res = service.cse().list(
                q='{}'.format(tag),
                cx='002626537913979718585:pkjl9_mtdpm',
                num = 10,
                start = index,
            ).execute()
            if 'items' not in res.keys():
                print("No results found after result {}. \n".format(index))
                result = ""
                end_search = True
            else:
                for result in res['items']:
                    lkd_result = {}
                    lkd_result['LinkedIn'] = result['link']
                    lkd_result['Tag'] = tag
                    output.append(lkd_result)
                index += 10
        except Exception as e:
            print(repr(e))
            end_search = True


# Fecha o arquivo e renomeia para evitar substituição
ddmdata.writecsv(output, 'output.csv')
now = datetime.datetime.now()
shutil.move("output.csv", "lkdSearch_output_" + now.strftime("%Y.%m.%d-%Hh%Mm") + ".csv")
print("Task complete.")