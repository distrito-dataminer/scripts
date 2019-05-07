import csv, re, sys, shutil

# Popula um dicionário com as informações do CSV
startupList = []
with open(r"C:\test\data.csv", encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)
    fh.close()

# Cria um CSV com as colunas relevantes para servir de output
all_keys = startupList[0].keys()
outputFile = open('output.csv', 'w', newline='', encoding = "utf8")
outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
outputWriter.writeheader()

for startup in startupList:
    for startup2 in startupList:
        if (startup['Site'] == startup2['Site'].replace('site.', '')) and (startup['Site'] != startup2['Site']):
            print("Site da {} igual ao site da {}".format(startup['Nome'],startup2['Nome']))