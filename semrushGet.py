from utils import cleaner, ddmdata, privatekeys

import os
import requests
import sys

key = privatekeys.semrush_key

display_date = '2019-10-01'
startup_list = cleaner.clean(ddmdata.readcsv(sys.argv[1]))
startup_list = [startup for startup in startup_list if startup['Site'] != '']
if 'Tirar?' in startup_list[0]:
    startup_list = [startup for startup in startup_list if startup['Tirar?'] == '']

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

#if len(startup_list) > 1000:
#    startup_list = startup_list[0:999]

if len(startup_list) > 100:
    chunk_list = []
    for chunk in chunks(startup_list, 100):
        chunk_list.append(chunk)
    print('Sample too large. Dividing into {} chunks.'.format(len(chunk_list)))
else:
    chunk_list = [startup_list]
    
csv_list = []

for i in range(0, len(chunk_list)):
    
    domain_string = ''

    for startup in chunk_list[i]:
        if 'Site final' in startup and startup['Site final']:
            site = startup['Site final']
        else:
            site = startup['Site']
        domain_string = domain_string + startup['Site'] + ','

    domain_string = domain_string.strip(',')

    print('Making API call #{}'.format(i+1))
    api_request = 'https://api.semrush.com/analytics/ta/v2/?type=traffic_summary&domains={}&key={}&display_date={}'.format(domain_string, key, display_date)

    response = requests.get(api_request)

    csv_list.append(response.text)

header = csv_list[0].split('\n', 1)[0]
final_csv = header + '\n'

for result in csv_list:
    contents = result.split('\n', 1)[1]
    final_csv = final_csv + contents

with open('semrush_results.csv', 'w', encoding='utf8') as f:
    f.write(final_csv)
    f.close()

semrush_results = ddmdata.readcsv('semrush_results.csv', delimiter=';')

for startup in startup_list:
    for result in semrush_results:
        if 'Site final' in startup and startup['Site final'] and result['domain'] in startup['Site final']:
            result['Site final'] = startup['Site final']
            if 'ID' in startup and startup['ID']:
                result['ID'] = startup['ID']
            if 'ID Estudo' in startup and startup['ID Estudo']:
                result['ID Estudo'] = startup['ID Estudo']
        if result['domain'] in startup['Site']:
            result['Site'] = startup['Site']
            if 'ID' in startup and startup['ID']:
                result['ID'] = startup['ID']
            if 'ID Estudo' in startup and startup['ID Estudo']:
                result['ID Estudo'] = startup['ID Estudo']

for startup in startup_list:
    if 'ID' in startup and startup['ID']:
        for result in semrush_results:
            if startup['ID'] == result['ID']:
                for key in result:
                    if key not in ['Site', 'Site final', 'ID', 'ID Estudo']:
                        startup[key] = result[key]

ddmdata.writecsv(semrush_results, '{}_semrush_{}.csv'.format(sys.argv[1].replace('.csv', ''), display_date))
ddmdata.writecsv(startup_list, '{}_with_semrush_{}.csv'.format(sys.argv[1].replace('.csv', ''), display_date))
