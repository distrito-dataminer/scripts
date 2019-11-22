from serpapi.google_search_results import GoogleSearchResults
from utils import ddmdata, privatekeys, cleaner
import itertools
import sys
from more_itertools import unique_everseen as unique

key = privatekeys.serpapi_key
num_results = 100
start = 0
queries = [{'Número': '1', 'Demanda': '', 'Busca': 'site:br.linkedin.com/company "Brasília" + "startup"'}]
demanda = ''
location = 'Brazil'

if len(sys.argv) > 1:
    queries = ddmdata.readcsv(sys.argv[1])

full_results = []

for query in queries:

    print('\nFazendo busca: {}'.format(query['Busca']))

    while True:
        print('Buscando {} resultados começando pelo de número {}...'.format(num_results, start))
        client = GoogleSearchResults({"q": query['Busca'], "location": location, "api_key": key, "num": num_results, "start": start, "device": "desktop", "nfpr": 1, "filter": 1, "gl": "br"})
        search_result = client.get_dict()
        try:
            print('{} resultados encontrados.'.format(len(search_result['organic_results'])))
            for result in search_result['organic_results']:
                result['Busca'] = query['Busca']
                result['Demanda'] = query['Demanda']
                full_results.append(result)
            if len(search_result['organic_results']) < (num_results - 1):
                print('Busca terminou: não há mais resultados.\n')
                start = 0
                break
            else:
                start += num_results
        except Exception as e:
            print('Busca terminou: {}\n'.format(repr(e) if repr(e) != "KeyError('organic_results')" else 'não há mais resultados.'))
            start = 0
            break

for result in full_results:
    if 'link' in result and 'linkedin' in result['link']:
        result['LinkedIn'] = result['link']

full_results = cleaner.clean(full_results)

final_results = []

for result1 in full_results:
    if 'Dupe check' in result1:
        continue
    result1['Dupe check'] = 'Sim'
    for result2 in full_results:
        if result1['LinkedIn'] and result2['LinkedIn'] and result1['LinkedIn'] == result2['LinkedIn']:
            demandas = result1['Demanda'].split(',')
            buscas = result1['Busca'].split(',')
            new_demanda = result2['Demanda'].split(',')
            new_busca = result2['Busca'].split(',')
            all_demandas = list(unique(demandas + new_demanda))
            all_buscas = list(unique(buscas + new_busca))
            result1['Demanda'] = ','.join(all_demandas)
            result1['Busca'] = ','.join(all_buscas)
            result2['Dupe check'] = 'Sim'
    final_results.append(result1)


ddmdata.writecsv(final_results, 'serpapi_output.csv')