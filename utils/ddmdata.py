#! python3
# ddmdata.py - functions related to working with data

import csv

# Popula um dicionário com as informações do CSV
def readcsv(csvpath):
    startupList = []
    with open(csvpath, encoding="utf8") as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            startupList.append(row)
        fh.close()
    return startupList

def writecsv(startupList, csvpath='output.csv'):
    all_keys = startupList[0].keys()
    outputFile = open(csvpath, 'w', newline='', encoding="utf8")
    outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
    outputWriter.writeheader()
    outputWriter.writerows(startupList)