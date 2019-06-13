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
    all_keys = []
    for item in startupList:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)
    outputFile = open(csvpath, 'w', newline='', encoding="utf8")
    outputWriter = csv.DictWriter(outputFile, all_keys, delimiter=',')
    outputWriter.writeheader()
    outputWriter.writerows(startupList)

def datacomplete(masterSL, slaveSL):
    for master in masterSL:
        for slave in slaveSL:
            if master['Site'] == slave['Site']:
                slave['Found'] = 'YES'
                for key in master:
                    if key in slave:
                        if slave[key] != "":
                            if master[key] == "":
                                master[key] = slave[key]
                                print("Completando {} da {} com valor {}".format(key.upper(), master["Startup"].upper(), slave[key]))
    return masterSL