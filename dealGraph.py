from utils import ddmdata, cleaner
from more_itertools import unique_everseen as unique
import itertools
from unidecode import unidecode
import re

deals = ddmdata.readcsv('deals.csv')
excluded_investors = ['', '-']
top_investors = ['Monashees', 'Kaszek Ventures', 'Crescera Investimentos', 'Redpoint eventures', 'DGF Investimentos', 'Canary', 'e.Bricks Ventures',
                 'Astella Investimentos', 'Valor Capital Group', 'SP Ventures', 'Confrapar', 'Inseed Investimentos', 'CVentures', 'Bossa Nova Investimentos', 'CRP Companhia de Participações']
seed_investors = ['Canary', 'Inseed Investimentos', 'Bossa Nova']
seriesabc_investors = [x for x in top_investors if x not in seed_investors]

startup_list = [deal['Startup'].strip() for deal in deals]
investor_list = []
for deal in deals:
    investors = deal['Investors'].split(',')
    investor_list += [investor.strip() for investor in investors]
startup_list = sorted(list(unique(startup_list)))
investor_list = sorted(list(unique(investor_list)))

for investor in excluded_investors:
    if investor in investor_list:
        investor_list.remove(investor)

for investor in top_investors:
    if investor not in investor_list:
        print(investor)

duplicate_startups = []
for startup1, startup2 in itertools.combinations(startup_list, 2):
    clean_startup1 = re.sub(r'[\W_]*', '', unidecode(startup1.lower().replace(' ', '')))
    clean_startup2 = re.sub(r'[\W_]*', '', unidecode(startup2.lower().replace(' ', '')))
    if clean_startup1 == clean_startup2:
        duplicate_startups.append(startup1 + ' & ' + startup2)
if duplicate_startups:
    print('Essas startups podem ser duplicatas:')
    for item in duplicate_startups:
        print(item)

duplicate_investors = []
for investor1, investor2 in itertools.combinations(investor_list, 2):
    clean_investor1 = re.sub(r'[\W_]*', '', unidecode(investor1.lower().replace(' ', '')))
    clean_investor2 = re.sub(r'[\W_]*', '', unidecode(investor2.lower().replace(' ', '')))
    if clean_investor1 == clean_investor2:
        duplicate_investors.append(investor1 + ' & ' + investor2)
if duplicate_investors:
    print('Esses investidores podem ser duplicatas:')
    for item in duplicate_investors:
        print(item)


startup_dict_list = []
startup_id = 0

for startup in startup_list:
    startup_id += 1
    startup_dict = {'Startup ID': startup_id, 'Startup': startup}
    investors = []
    for deal in deals:
        if deal['Startup'].strip() == startup:
            new_investors = [investor.strip()
                             for investor in deal['Investors'].split(',')]
            investors += new_investors
    investors = sorted(list(unique(investors)))
    investors = [x for x in investors if x not in excluded_investors]
    startup_top_investors = [x for x in investors if x in top_investors]
    startup_dict['Investors'] = ','.join(investors)
    startup_dict['Top Investors'] = ','.join(startup_top_investors)
    startup_dict['Investor count'] = len(investors)
    startup_dict['Top Investor count'] = len(startup_top_investors)
    startup_dict_list.append(startup_dict)


investor_dict_list = []
investor_id = 0
investor_id_dict = {}

for investor in investor_list:
    investor_id += 1
    investor_dict = {'Investor ID': investor_id, 'Investor': investor}
    investor_id_dict[investor] = investor_id
    startups = []
    for startup in startup_dict_list:
        if investor in startup['Investors'].split(','):
            startups.append(startup['Startup'].strip())
    startups = sorted(list(unique(startups)))
    investor_dict['Startups'] = ','.join(startups)
    investor_dict['Startups invested'] = len(startups)
    if investor in top_investors:
        investor_dict['Top Investor'] = 1
    else:
        investor_dict['Top Investor'] = 0
    if investor in seriesabc_investors:
        investor_dict['Series'] = 2
    elif investor in seed_investors:
        investor_dict['Series'] = 1
    else:
        investor_dict['Series'] = 0
    investor_dict_list.append(investor_dict)

relationship_list = []

for startup in startup_dict_list:
    startup_investors = sorted(startup['Investors'].split(','))
    if len(startup_investors) >= 2:
        for investor1, investor2 in itertools.combinations(startup_investors, 2):
            relationship_dict = {'Source': investor1, 'Target': investor2}
            relationship_list.append(relationship_dict)

edges = []
relationships = []

for item in list(unique(relationship_list)):
    weight = relationship_list.count(item)
    edge = {'Source': investor_id_dict[item['Source']],
            'Target': investor_id_dict[item['Target']], 'Type': 'Undirected', 'Weight': weight}
    relationship = {
        'Source': item['Source'], 'Target': item['Target'], 'Type': 'Undirected', 'Weight': weight}
    edges.append(edge)
    relationships.append(relationship)

nodes = []

for investor in investor_dict_list:
    node = {'Id': investor['Investor ID'], 'Label': investor['Investor'],
            'Size': investor['Startups invested'], 'Top Investor': investor['Top Investor'], 'Series': investor['Series']}
    nodes.append(node)


ddmdata.writecsv(startup_dict_list, 'startups_investors.csv')
ddmdata.writecsv(investor_dict_list, 'investors_startups.csv')
ddmdata.writecsv(relationships, 'investor_relationships.csv')
ddmdata.writecsv(edges, 'investor_edges.csv')
ddmdata.writecsv(nodes, 'investor_nodes.csv')
