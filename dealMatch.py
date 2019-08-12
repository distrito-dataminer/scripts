#! python3
# dealMatch.py - referencia a base compilada à base de Deals

from utils import ddmdata, cleaner
import sys, re
from more_itertools import unique_everseen as unique

deals = ddmdata.readcsv(sys.argv[1])
base = ddmdata.readcsv(sys.argv[2])
command = sys.argv[3]

deals = cleaner.clean(deals)
base = cleaner.clean(base)

if command == 'dealid':
    for deal in deals:
        idlist = []
        for startup in base:
            if deal['Site'] and (deal['Site'] == startup['Site']):
                idlist.append(startup['ID'])
            elif deal['Startup'] == startup['Startup']:
                idlist.append(startup['ID'])
        idlist = list(unique(idlist))
        if len(idlist) > 1:
            print('{} has more than one ID! {}'.format(deal['Startup'], ', '.join(idlist)))
        deal['ID'] = ';'.join(idlist)

    ddmdata.writecsv(deals, 'deals_matched.csv')

if command == 'funding':

    ignoreList = ['Acquisition', 'Debt Financing', 'Secondary Market', 'Convertible Note', 'Fusão', 'IPO']

    for startup in base:
        startupdeals = []
        for deal in deals:
            if startup['ID'] in deal['ID'].split(';'):
                startupdeals.append(deal)
        if startupdeals:
            funding = 0
            for deal in startupdeals:
                if deal['Funding'] not in ignoreList:
                    try:
                        funding += int(re.sub('[^\d]', '', deal['Valor da Rodada (em USD)']))
                    except Exception as e:
                        print(repr(e))
                        continue
            startup['Funding total'] = funding

    ddmdata.writecsv(base, 'base_com_funding.csv')
