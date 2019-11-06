#! python3
# dealMatch.py - referencia a base compilada à base de Deals

from utils import ddmdata, cleaner
import sys, re
from more_itertools import unique_everseen as unique

deals = ddmdata.readcsv(sys.argv[1])
base = ddmdata.readcsv(sys.argv[2])
command = sys.argv[3]
id_type = 'ID'

deals = cleaner.clean(deals)
base = cleaner.clean(base)

if command == 'dealid':
    for deal in deals:
        idlist = []
        for startup in base:
            if startup['Tirar?']:
                continue
            if deal['Site'] and (deal['Site'] == startup['Site']):
                idlist.append(startup[id_type])
            elif cleaner.bare(deal['Startup']) == cleaner.bare(startup['Startup']):
                idlist.append(startup[id_type])
        idlist = list(unique(idlist))
        while '' in idlist:
            idlist.remove('')
        if len(idlist) > 1:
            print('{} has more than one ID! {}'.format(deal['Startup'], ', '.join(idlist)))
        deal[id_type] = ';'.join(idlist)

    ddmdata.writecsv(deals, 'deals_matched.csv')

if command == 'funding':

    ignoreList = ['Acquisition', 'Debt Financing', 'Secondary Market', 'Convertible Note', 'Fusão', 'IPO']

    for startup in base:
        startupdeals = []
        for deal in deals:
            if startup[id_type] in deal[id_type].split(';'):
                startupdeals.append(deal)
        if startupdeals:
            funding = 0
            for deal in startupdeals:
                if deal['Valor da Rodada (em USD)'] and deal['Funding'] and deal['Funding'] not in ignoreList:
                    if deal['Valor da Rodada (em USD)'] != '-':
                        try:
                            funding += int(re.sub('[^\d]', '', deal['Valor da Rodada (em USD)']))
                        except Exception as e:
                            print(repr(e))  
                            continue
            startup['Funding total'] = funding

    ddmdata.writecsv(base, 'base_com_funding.csv')
