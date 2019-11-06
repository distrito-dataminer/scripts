import requests, re, os
from time import sleep

cookies = {
    '__cfduid': 'd53d3d318f72b850c260ce025e26c8ed01559138462',
    'ajs_user_id': 'null',
    'ajs_group_id': 'null',
    'ajs_anonymous_id': '%22ea692015-6878-441f-ba38-b5fd2da9725b%22',
    'amplitude_idundefinedstartupbase.com.br': 'eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==',
    'amplitude_id_6a8740dce503847cdd85869511f54a8astartupbase.com.br': 'eyJkZXZpY2VJZCI6IjhlNGNkNGRmLTI1MGItNGRjYS04N2Q4LTNlODIzYmMyZGUyMVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU3MjUyNzk0NzU4MywibGFzdEV2ZW50VGltZSI6MTU3MjUyNzk1MzgwMywiZXZlbnRJZCI6NSwiaWRlbnRpZnlJZCI6NCwic2VxdWVuY2VOdW1iZXIiOjl9',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://startupbase.com.br/',
    'Authorization': 'Bearer bGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGFydHVwYkwMjJ9.wlurgMdOY62GhvAFxcLrQBtpx-_t75sP0yAM',
    'Origin': 'https://startupbase.com.br',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

with open('sb_search_html.html', 'r', encoding='utf8') as f:
    search_html = f.read()
    f.close()

slug_regex = re.compile(r'"/c/startup/([^"]+)"')
slugs = re.findall(slug_regex, search_html)
already_scraped = [file.replace('.json', '') for file in os.listdir('C:\\Test\\SB\\')]
final_slugs = [slug for slug in slugs if slug not in already_scraped]
if len(slugs) != len(final_slugs):
    print('Out of {} startups, {} startups were already scraped and will not be redone.'.format(len(slugs), len(slugs) - len(final_slugs)))
slug_jsons = {}


for slug in final_slugs:
    try:
        print('Getting info for {}...'.format(slug))
        response = requests.get('https://api-leg.startupbase.com.br/startups/slug/{}'.format(slug), headers=headers, cookies=cookies, timeout=5)
        print('Status code: {}'.format(response.status_code))
        slug_jsons[slug] = response.text
        try:
            with open('C:\\Test\\SB\\{}.json'.format(slug), 'w', encoding='utf8') as f:
                f.write(response.text)
                f.close()
        except Exception as e:
            print(repr(e))
            continue
    except Exception as e:
        print(repr(e))
        continue