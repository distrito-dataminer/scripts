from utils import ddmdata, cleaner
import os, sys

mypath = sys.argv[1]

kpiList = []

for filename in os.listdir(mypath):
    kpi = {}
    kpi['Data'] = filename.replace('Base Compilada - Startups - ', '').replace('.csv', '').replace('.', '-')
    base = ddmdata.readcsv(os.path.join(mypath, filename))
    base = cleaner.clean(base)
    base = cleaner.score(base)
    startup_count = 0
    removed = 0
    ndp_list = []
    checked = 0
    cnpj = 0
    linkedin = 0
    end = 0
    email = 0
    setor = 0
    publico = 0
    for startup in base:
        startup_count += 1
        if 'Checado' in startup and startup['Checado']:
            checked += 1
        if 'Tirar?' in startup and startup['Tirar?']:
            removed += 1
        else:
            if startup['NDP']:
                ndp_list.append(int(startup['NDP']))
        if startup['CNPJ']:
            cnpj += 1
        if startup['LinkedIn']:
            linkedin += 1
        if startup['Endereço']:
            end += 1
        if 'E-mail' in startup and startup['E-mail']:
            email += 1
        if startup['Setor']:
            setor += 1
        if startup['Público']:
            publico += 1
    kpi['Total na base'] = startup_count
    kpi['Checadas'] = checked
    kpi['Removidas'] = removed
    kpi['Total sem removidas'] = (startup_count - removed)
    kpi['NDP Médio'] = round(sum(ndp_list) / len(ndp_list), 2)
    kpi['Maior NDP'] = max(ndp_list)
    kpi['Menor NDP'] = min(ndp_list)
    kpi['Com CNPJ'] = cnpj
    kpi['Com LinkedIn'] = linkedin
    kpi['Com Endereço'] = end
    kpi['Com E-mail'] = email
    kpi['Com Setor'] = setor
    kpi['Com Público'] = publico
    kpiList.append(kpi)

ddmdata.writecsv(kpiList, 'kpis.csv')
        


    