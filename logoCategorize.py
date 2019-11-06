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

if len(sys.argv) >= 4:
    destPath = sys.argv[3]
    destPath = os.path.abspath(destPath)
    if destPath[-1] != '\\':
        destPath += '\\'
    if not os.path.exists(destPath):
        os.mkdir(destPath)
else:
    destPath = logoPath

logore = re.compile(r'(^.*)(\..*?$)')

foundLogos = []
logoList = []
dupeLogos = []
no_logo = []
for filename in os.listdir(logoPath):
    logoList.append(filename)

for startup in startupList:
    nome = startup['Startup']
    nomeClean = re.sub(r'[^\w]', '', unidecode(nome.lower().strip()))
    startup['LogoFound'] = False
    
    for logo in logoList:

        mo = logore.search(logo)
        
        if mo:
            filename = mo.group(1)
            extension = mo.group(2)
            filenameClean = re.sub(r'[^\w]', '', unidecode(filename.lower().strip()))
            
        if nomeClean == filenameClean:
            if startup['LogoFound'] == True:
                dupeLogos.append(logo)
                if not os.path.exists(destPath + 'Duplicatas\\'):
                    os.mkdir(destPath + 'Duplicatas\\')
                shutil.copy(logoPath+logo, destPath + 'Duplicatas\\' + logo)
            else:
                startup['LogoFound'] = True
                foundLogos.append(logo)
                if not os.path.exists(destPath + startup['Categoria'].strip()):
                    os.mkdir(destPath + startup['Categoria'].strip())
                if not os.path.exists(destPath + startup['Categoria'].strip()+'\\'+startup['Subcategoria'].strip()):
                    os.mkdir(destPath + startup['Categoria'].strip()+'\\'+startup['Subcategoria'].strip())
                shutil.copy(logoPath+logo, destPath + startup['Categoria'].strip()+'\\'+startup['Subcategoria'].strip()+'\\'+ logo)

logoList = sorted(logoList, key=str.casefold)

print('\nLOGOS QUE ESTÃO SEM STARTUP:')
for logo in logoList:
    if logo not in foundLogos:
        print(logo)

dupeLogos = sorted(dupeLogos, key=str.casefold)

print('\nLOGOS DUPLICADOS:')
for logo in dupeLogos:
    print(logo)

print('\nSTARTUPS QUE ESTÃO SEM LOGO:')
for startup in startupList:
    if startup['LogoFound'] == False:
        no_logo.append(startup['Startup'])
no_logo = sorted(no_logo, key=str.casefold)
for item in no_logo:
    print(item)
