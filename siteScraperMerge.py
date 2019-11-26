from utils import cleaner, ddmdata
import os
import sys
from more_itertools import unique_everseen as unique

startup_list = cleaner.clean(ddmdata.readcsv(sys.argv[1]))
sl_name = sys.argv[1].replace('.csv', '')
ss_results = ddmdata.readcsv(sys.argv[2])

#Initializes the result groups list and index dict which will group base URLs together
result_groups = []
index_dict = {}
current_index = 0

#Groups results of the same base URL in a list of lists
for result in ss_results:
    base_url = result['base_url']
    if base_url in index_dict:
        result_groups[index_dict[base_url]].append(result)
    else:
        index_dict[base_url] = current_index
        result_list = [result]
        result_groups.append(result_list)
        current_index += 1

final_results = []

for result_group in result_groups:

    final_result = {}
    cnpj_list = []
    facebook_list = []
    linkedin_list = []
    twitter_list = []
    instagram_list = []
    email_list = []

    for result in result_group:

        cnpj_list += result['cnpj_all'].split(',')
        facebook_list += result['facebook_all'].split(',')
        linkedin_list += result['linkedin_all'].split(',')
        twitter_list += result['twitter_all'].split(',')
        instagram_list += result['instagram_all'].split(',')
        email_list += result['email_all'].split(',')

        if len(result_group) == 1 or result['depth'] == '0':
            final_result['Response'] = result['response']
            final_result['base_url'] = result['base_url']
            final_result['final_url'] = result['final_url']
            if result['final_url']:
                final_result['Site final'] = cleaner.clean_site(result['final_url'])
            else:
                final_result['Site'] = cleaner.clean_site(result['base_url'])

    final_result['CNPJ'] = ','.join(sorted(list(unique(cnpj_list))))
    final_result['Facebook'] = ','.join(sorted(list(unique(facebook_list))))
    final_result['LinkedIn'] = ','.join(sorted(list(unique(linkedin_list))))
    final_result['Twitter'] = ','.join(sorted(list(unique(twitter_list))))
    final_result['Instagram'] = ','.join(sorted(list(unique(instagram_list))))
    final_result['E-mail'] = ','.join(sorted(list(unique(email_list))))

    final_results.append(final_result)

final_results = cleaner.clean(final_results)

add_keys = ['Facebook', 'LinkedIn', 'Twitter', 'Instagram', 'E-mail']
replace_keys = ['Site final', 'Response']
add_if_empty_keys = ['CNPJ']

for startup in startup_list:
    clean_site = cleaner.clean_site(startup['Site'])
    for result in final_results:
        result_site = cleaner.clean_site(result['base_url'])
        if clean_site == result_site:
            for key in add_keys:
                current_list = startup[key].split(',')
                new_list = result[key].split(',')
                final_list = sorted(list(unique(current_list + new_list)))
                while '' in final_list:
                    final_list.remove('')
                startup[key] = ','.join(final_list)
            for key in replace_keys:
                new_list = result[key].split(',')
                final_list = sorted(list(unique(new_list)))
                while '' in final_list:
                    final_list.remove('')
                startup[key] = ','.join(final_list)
            for key in add_if_empty_keys:
                if not startup[key]:
                    new_list = result[key].split(',')
                    final_list = sorted(list(unique(new_list)))
                    while '' in final_list:
                        final_list.remove('')
                    startup[key] = ','.join(final_list)

error_list = ['DNSLookupError', 'ResponseNeverReceived', 'TimeoutError']

for startup in startup_list:
    for error in error_list:
        if error in startup['Response']:
            startup['Response'] = error

ddmdata.writecsv(startup_list, '{}_ss_merged.csv'.format(sl_name))
