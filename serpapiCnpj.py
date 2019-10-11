from serpapi.google_search_results import GoogleSearchResults
from utils import ddmdata, privatekeys

key = privatekeys.serpapi_key
num_results = 1
start = 0
location = 'Brazil'

sample = ddmdata.readcsv('sample.csv')

for startup in sample:
    print('Pegando CNPJ de {}'.format(startup['Startup']))
    clean_site = startup['Site'].lower().replace('http://', '')
    query = 'site:empresascnpj.com "{}"'.format(clean_site)
    client = GoogleSearchResults({"q": query, "location": location, "api_key": key, "num": num_results, "start": start, "device": "desktop", "nfpr": 1, "filter": 1, "gl": "br"})
    search_result = client.get_dict()
    if 'organic_results' in search_result:
        if 'link' in search_result['organic_results'][0] and 'snippet' in search_result['organic_results'][0]:
            snippet = search_result['organic_results'][0]['snippet']
            if clean_site in snippet:
                cnpj = search_result['organic_results'][0]['link'].split('/')[-1]
                try:
                    cnpj = "{}.{}.{}/{}-{}".format(
                                    cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])
                except Exception as e:
                    print(e)
                startup['CNPJ Bot'] = cnpj
                print(cnpj)
                if cnpj == startup['CNPJ']:
                    startup['CNPJ Igual?'] = 'Sim'
                else:
                    startup['CNPJ Igual?'] = 'Não'

ddmdata.writecsv(sample, 'serpapi_cnpjs.csv')