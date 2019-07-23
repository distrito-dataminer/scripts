from utils import ddmdata
import os, csv, re, sys, shutil
from unidecode import unidecode

csvPath = sys.argv[1]
startupList = ddmdata.readcsv(csvPath)

csvName = csvPath.replace('.csv', '')

logoPath = sys.argv[2]
logoPath = os.path.abspath(logoPath)
if logoPath[-1] != '\\':
    logoPath += '\\'

logore = re.compile(r'(^.*)(\..*?$)')

logoList = []
for filename in os.listdir(logoPath):
    logoList.append(filename)

for startup in startupList:
    nome = startup['Startup']
    nomeClean = re.sub(r'[^\w]', '', unidecode(nome.lower().strip()))
    
    for logo in logoList:
        
        if startup['Logo'] == 'TRUE':
            break
            
        mo = logore.search(logo)
        
        if mo:
            filename = mo.group(1)
            extension = mo.group(2)
            filenameClean = re.sub(r'[^\w]', '', unidecode(filename.lower().strip()))
            
        if nomeClean == filenameClean:
            startup['Logo'] = 'TRUE'
            if not os.path.exists(logoPath+csvName+'\\'):
                os.mkdir(logoPath+csvName+'\\')
            shutil.copy(logoPath+logo, logoPath+csvName+'\\'+logo)

ddmdata.writecsv(startupList, sys.argv[1].replace('.csv', '') + '_logos_checked.csv')