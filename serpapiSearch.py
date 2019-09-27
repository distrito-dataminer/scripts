from serpapi.google_search_results import GoogleSearchResults
from utils import ddmdata, privatekeys

key = privatekeys.serpapi_key
num_results = 100
start = 0

query = 'site:linkedin.com/company "startup" + "são paulo"'
location = 'Brazil'

full_results = []

while True:
    client = GoogleSearchResults({"q": query, "location": location, "api_key": key, "num": num_results, "start": start, "device": "desktop", "nfpr": 1, "filter": 1, "gl": "br"})
    search_result = client.get_dict()
    if 'organic_results' in search_result:
        for result in search_result['organic_results']:
            full_results.append(result)
        start += num_results
    else:
        break

for result in full_results:
    if 'link' in result:
        result['LinkedIn'] = result['link']

ddmdata.writecsv(full_results, 'serpapi_output.csv')