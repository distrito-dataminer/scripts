#! python3
# dataSearch.py - searches for startups containing terms in their tags or description.

import sys
import re
from utils import ddmdata
from more_itertools import unique_everseen as unique
from pprint import pprint, pformat
from collections import OrderedDict
from unidecode import unidecode

startup_list = ddmdata.readcsv(sys.argv[1])
full_output = False

if len(sys.argv) >= 3:
    search_items = ddmdata.readcsv(sys.argv[2])
else:
    search_items = [{'Número': '1',
                     'Demanda': 'Santa Catarina',
                     'Tags': 'Florianópolis, Joinville, Blumenau, Chapecó, Itajaí, Criciúma, Jaraguá do Sul, Palhoça, Lages, Camboriú, Brusque, Tubarão, São Bento do Sul, Navegantes'}]

if len(sys.argv) >=4 and sys.argv[3] == 'fullout':
    full_output = True


for item in search_items:

    print('\nRunning search for {} - {}'.format(item['Número'], item['Demanda']))
    print('Tags: {}\n'.format(item['Tags']))

    tag_matches = []
    description_matches = []
    tnd_matches = []
    category_matches = []
    sector_matches = []

    tag_dict = {}
    desc_dict = {}
    cat_dict = {}

    search_terms = item['Tags'].split(',')

    search_terms = [unidecode(term.lower().strip()) for term in search_terms]

    for term in search_terms:
        tag_dict[term] = 0
        desc_dict[term] = 0
        cat_dict[term] = 0

    for startup in startup_list:
        if startup['Tirar?'] != '':
            continue
        match_count = 0
        matched_in = []
        for term in search_terms:
            term_pattern = re.compile('\\b{}\\b'.format(term), re.IGNORECASE)
            if re.search(term_pattern, unidecode(startup['Tags'])):
                tag_matches.append(startup)
                tag_dict[term] += 1
                match_count += 1
                matched_in.append('Tags')
            if re.search(term_pattern, unidecode(startup['Descrição'])):
                description_matches.append(startup)
                desc_dict[term] += 1
                match_count += 1
                matched_in.append('Descrição')
            if re.search(term_pattern, unidecode(startup['Categoria'])) or re.search(term_pattern, unidecode(startup['Subcategoria'])):
                category_matches.append(startup)
                cat_dict[term] += 1
                match_count += 1
                matched_in.append('Categoria')
        startup['Match Count'] = match_count
        startup['Matched in'] = ','.join(list(unique(matched_in)))

    tnd_matches = [match for match in tag_matches if match in description_matches]

    # Makes sure there are no repeated elements in each list
    tag_matches = list(unique(tag_matches))
    description_matches = list(unique(description_matches))
    tnd_matches = list(unique(tnd_matches))
    category_matches = list(unique(category_matches))
    main_matches = list(unique(sector_matches + category_matches + tnd_matches))
    all_matches = list(unique(main_matches + tag_matches + description_matches))

    # Sorts dictionaries by number of matches, descending
    tag_dict = sorted(tag_dict.items(), key=lambda kv: kv[1], reverse=True)
    desc_dict = sorted(desc_dict.items(), key=lambda kv: kv[1], reverse=True)
    cat_dict = sorted(cat_dict.items(), key=lambda kv: kv[1], reverse=True)

    # Outputs match stats to a file
    with open('0_Match_Stats.txt', 'a+', encoding='utf8') as f:
        f.write('\n\n---------------------------------------------------------------')
        f.write('\nSTATS FOR {} - {}\n'.format(item['Número'], item['Demanda']))
        f.write('\nTag matches: {}'.format(len(tag_matches)))
        f.write('\nDescription matches: {}'.format(len(description_matches)))
        f.write('\nTag and Description matches: {}'.format(len(tnd_matches)))
        f.write('\nCategory matches: {}'.format(len(category_matches)))
        f.write('\nAll matches: {}'.format(len(all_matches)))
        f.write('\n\nTag frequency:\n')
        f.write(pformat(tag_dict))
        f.write('\n\nDescription frequency:\n')
        f.write(pformat(desc_dict))
        f.write('\n\nCategory frequency:\n')
        f.write(pformat(cat_dict))
        f.write('\n---------------------------------------------------------------\n\n')

    if full_output:
        if tag_matches:
            ddmdata.writecsv(tag_matches, '{}_{}_Matches_Tags.csv'.format(item['Número'], item['Demanda']))
        if description_matches:
            ddmdata.writecsv(description_matches, '{}_{}_Matches_Descrição.csv'.format(item['Número'], item['Demanda']))
        if tnd_matches:
            ddmdata.writecsv(tnd_matches, '{}_{}_Matches_Tags&Descrição.csv'.format(item['Número'], item['Demanda']))
        if category_matches:
            ddmdata.writecsv(category_matches, '{}_{}_Matches_Categoria.csv'.format(item['Número'], item['Demanda']))
        if main_matches:
            ddmdata.writecsv(main_matches, '{}_{}_Matches_Main.csv'.format(item['Número'], item['Demanda']))
    if all_matches:
        ddmdata.writecsv(all_matches, '{}_{}_Matches_All.csv'.format(item['Número'], item['Demanda']))

print('Task completed successfully.')