#! python3
# linkToLinkedin.py - Obtém URLs do Linkedin a partir de uma lista de sites por meio do Google Custom Search
# Uso - python linkToLinkedin.py [csv] [opcional: noreplace] <- não substitui informações já presentes no csv
# Exemplo: python linkToLinkedin.py startups.csv noreplace

import sys, csv, shutil, datetime
from googleapiclient.discovery import build

# Conecta na API do Google com a chave de API providenciada
service = build("customsearch", "v1", developerKey="AIzaSyCitxXqhnfeZdhiw85he62pRu_LGm_0wzU")

file = sys.argv[1]
noReplace = False
if len(sys.argv) > 2 and sys.argv[2].lower() == "noreplace":
    noReplace = True

# Popula um dicionário com os dados de startups do csv
startupList = []
with open(file, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)

# Cria um csv com as colunas relevantes para servir de output
if 'LinkedIn' not in startupList[0]:
    startupList[0]["LinkedIn"] = ""
startupList[0]['Revisar LinkedIn'] = ""
all_keys = startupList[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()

# Faz uma busca com o site da startup como query no LinkedIn
for startup in startupList:
    if (noReplace == True) and "LinkedIn" in startup.keys():
        if (startup['LinkedIn'] != ("" or "null")):
            print("LinkedIn for " + startup['Nome'] + " already present.\n")
            startup['Revisar LinkedIn'] = "NÃO"
            outputWriter.writerow(startup)
            continue
    print("Getting LinkedIn for " + startup['Nome'] + "...")
    res = service.cse().list(
      q=startup['Site'],
      cx='002626537913979718585:pkjl9_mtdpm',
      num = 1,
    ).execute()
    if 'items' not in res.keys():
        print("No results. \n")
        result = "NÃO ENCONTRADO"
    else:
        result = res['items'][0]['link']
        print("Found Linkedin: " + result + '\n')
    startup['LinkedIn'] = result
    startup['Revisar LinkedIn'] = "SIM"
    outputWriter.writerow(startup)

# Fecha o arquivo e renomeia para evitar substituição
outputFile.close()
print("Task complete.")
now = datetime.datetime.now()
shutil.move("output.csv", "output " + now.strftime("%Y-%m-%d %Hh%Mm") + ".csv")