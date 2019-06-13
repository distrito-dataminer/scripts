from utils import cleaner, ddmdata
import csv, re

base = ddmdata.readcsv('base.csv')
novas = ddmdata.readcsv('abs.csv')

base = cleaner.clean(cleaner.clean(base))
novas = cleaner.clean(cleaner.clean(novas))
verified = []
nonverified = []
newstartups = []

for startup in base:
    for newstartup in novas:
        if startup['Site'] == newstartup['Site']:
            newstartup['Found'] = 'Yes'
            if newstartup['Verified'] == 'check':
                print('Completando dados de startup verificada: {}'.format(startup['Startup']))
                verified.append(newstartup['Site'])
                if newstartup['Público']:
                    startup['Público'] = newstartup['Público']
                if newstartup['Modelo de negócio']:
                    startup['Modelo de negócio'] = newstartup['Modelo de negócio']
                if newstartup['Descrição']:
                    if startup['Descrição']:
                        startup['Descrição'] += '\n\n' + newstartup['Descrição']
                    else:
                        startup['Descrição'] = newstartup['Descrição']
                tags = startup['Tags'].split(',')
                newtags = newstartup['Tags'].split(',')
                if newstartup['Setor']:
                    newtags.append(newstartup['Setor'])
                finaltags = list(set(tags).union(set(newtags)))
                startup['Tags'] = ','.join(finaltags)
                if newstartup['Estado']:
                    startup['Estado'] = newstartup['Estado']
                if newstartup['Cidade']:
                    startup['Cidade'] = newstartup['Cidade']
                if newstartup['Facebook']:
                    startup['Facebook'] = newstartup['Facebook']
                if newstartup['LinkedIn']:
                    startup['LinkedIn'] = newstartup['LinkedIn']
                if newstartup['Instagram']:
                    startup['Instagram'] = newstartup['Instagram']
                if newstartup['Endereço']:
                    startup['Endereço'] = newstartup['Endereço']
                if newstartup['Porte LKD']:
                    startup['Porte LKD'] = newstartup['Porte LKD']
            else:
                print('Completando dados de startup não-verificada: {}'.format(startup['Startup']))
                nonverified.append(newstartup['Site'])
                if newstartup['Público'] and not startup['Público']:
                    startup['Público'] = newstartup['Público']
                if newstartup['Modelo de negócio'] and not startup['Modelo de negócio']:
                    startup['Modelo de negócio'] = newstartup['Modelo de negócio']
                if newstartup['Descrição'] and not startup['Descrição']:
                    startup['Descrição'] = newstartup['Descrição']
                tags = startup['Tags'].split(',')
                newtags = newstartup['Tags'].split(',')
                if newstartup['Setor']:
                    newtags.append(newstartup['Setor'])
                finaltags = list(set(tags).union(set(newtags)))
                startup['Tags'] = ','.join(finaltags)
                if newstartup['Estado'] and not startup['Estado']:
                    startup['Estado'] = newstartup['Estado']
                if newstartup['Cidade'] and not startup['Cidade']:
                    startup['Cidade'] = newstartup['Cidade']
                if newstartup['Facebook'] and not startup['Facebook']:
                    startup['Facebook'] = newstartup['Facebook']
                if newstartup['LinkedIn'] and not startup['LinkedIn']:
                    startup['LinkedIn'] = newstartup['LinkedIn']
                if newstartup['Instagram'] and not startup['Instagram']:
                    startup['Instagram'] = newstartup['Instagram']
                if newstartup['Endereço'] and not startup['Endereço']:
                    startup['Endereço'] = newstartup['Endereço']
                if newstartup['Porte LKD'] and not startup['Porte LKD']:
                    startup['Porte LKD'] = newstartup['Porte LKD']

for startup in novas:
    if 'Found' not in startup:
        newstartups.append(startup['Site'])
        startup['Fonte'] = 'StartupBase'
        base.append(startup)
        tags = startup['Tags'].split(',')
        tags.append(startup['Setor'])
        startup['Tags'] = ','.join(tags)
        startup['Setor'] = ''

ddmdata.writecsv(base, 'teste.csv')

with open('verified.txt', 'w') as f:
    f.write('\n'.join(verified))
    f.close()

with open('nonverified.txt', 'w') as f:
    f.write('\n'.join(nonverified))
    f.close()

with open('newstartups.txt', 'w') as f:
    f.write('\n'.join(newstartups))
    f.close()