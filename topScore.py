from utils import cleaner, ddmdata
import sys
import re

startup_list = cleaner.clean(ddmdata.readcsv(sys.argv[1]))
study_name = sys.argv[2]

id_type = 'ID'

for startup in startup_list:
    if 'ID' not in startup or not startup['ID']:
        print('ID missing in one or more startups. Trying ID Estudo.')
        for startup in startup_list:
            if 'ID Estudo' not in startup or not startup['ID Estudo']:
                raise ValueError('Every startup must have an ID or ID Estudo.')
        id_type = 'ID Estudo'

emp_count_dict = {
        '0-1': 1,
        '1-5': 3,
        '1-10': 4,
        '2-10': 5,
        '6-10': 8,
        '11-20': 15,
        '11-50': 20,
        '21-50': 30,
        '51-200': 100,
        '201-500': 250,
        '501-1000': 600,
        '1001-5000': 1500}

revenue_dict = {
        'Outro': 0,
        'Até R$20.000': 10000,
        'De R$20.001 a R$60.000': 20000,
        'De R$60.001 a R$160.000': 60000,
        'Até 360k': 150000,
        'De R$160.001 a R$260.000': 160000,
        'De R$260.001 a R$360.000': 260000,
        'De R$360.001 a R$720.000': 360000,
        'De R$720.001 a R$1.000.000': 720000,
        'De R$1.000.001 a R$1.800.000': 1000000,
        '360k - 5M': 1000000,
        'De R$1.800.001 a R$3.600.000': 1800000,
        'De R$3.600.001 a R$5.000.000': 3600000,
        'De R$5.000.001 a R$10.000.000': 5000000,
        'De R$10.000.001 a R$25.000.000': 10000000,
        '5M - 30M': 10000000,
        'De R$25.000.001 a R$50.000.000': 25000000,
        'De R$50.000.001 a R$100.000.000': 50000000,
        'Acima de R$100.000.000': 100000000}

scorable_list = []

for startup in startup_list:

    scorable = {'ID': startup[id_type]}

    # Make sure everyone has an employee count and standardize into ints
    if 'Funcionários LKD' in startup and startup['Funcionários LKD']:
        scorable['employees'] = int(startup['Funcionários LKD'])
    elif 'Porte LKD' in startup and startup['Porte LKD']:
        scorable['employees'] = emp_count_dict[startup['Porte LKD'].replace(
            ' ', '')]
    elif 'Faixa # de funcionários' in startup and startup['Faixa # de funcionários']:
        scorable['employees'] = emp_count_dict[startup['Faixa # de funcionários'].replace(
            ' ', '')]
    else:
        scorable['employees'] = 0

    # Make sure everyone has funding and standardize into ints
    if 'Funding total' in startup and startup['Funding total']:
        funding = re.sub(r'[^\d]', '', startup['Funding total'])
        scorable['funding'] = int(funding)
    else:
        scorable['funding'] = 0

    # Make sure everyone has followers and standardize into ints
    if 'Seguidores LKD' in startup and startup['Seguidores LKD']:
        scorable['lkd_followers'] = int(startup['Seguidores LKD'])
    else:
        scorable['lkd_followers'] = 0

    # Make sure everyone has web traffic and standardize into ints
    if 'total_visits' in startup and startup['total_visits']:
        total_visits = re.sub(r'[^\d]', '', startup['total_visits'])
        if total_visits:
            scorable['traffic'] = int(total_visits)
        else:
            scorable['traffic'] = 0
    else:
        scorable['traffic'] = 0

    # Make sure everyone has presumed revenue and standardize into ints
    if 'Faturamento declarado' in startup and startup['Faturamento declarado'] not in ['', 'N/D', '0']:
        try:
            lower_bound, upper_bound = startup['Faturamento declarado'].replace(' ', '').split('-')
            revenue = (int(lower_bound) + int(upper_bound)) / 2
            scorable['revenue'] = int(revenue)
        except:
            print('Exception when processing Faturamento declarado for {}. Value was {}. Proceeding.'.format(startup['Startup'], startup['Faturamento declarado']))
    if 'Faturamento Presumido' in startup and startup['Faturamento Presumido']:
        scorable['revenue'] = revenue_dict[startup['Faturamento Presumido']]
    else:
        scorable['revenue'] = 0

    scorable_list.append(scorable)
    
#Rank by these factors and add up score
all_revenues = sorted([scorable['revenue'] for scorable in scorable_list], reverse=True)
all_employees = sorted([scorable['employees'] for scorable in scorable_list], reverse=True)
all_funding = sorted([scorable['funding'] for scorable in scorable_list], reverse=True)
all_followers = sorted([scorable['lkd_followers'] for scorable in scorable_list], reverse=True)
all_traffic = sorted([scorable['traffic'] for scorable in scorable_list], reverse=True)

for scorable in scorable_list:
    scorable['revenue_rank'] = all_revenues.index(scorable['revenue'])
    scorable['employees_rank'] = all_employees.index(scorable['employees'])
    scorable['funding_rank'] = all_funding.index(scorable['funding'])
    scorable['followers_rank'] = all_followers.index(scorable['lkd_followers'])
    scorable['traffic_rank'] = all_traffic.index(scorable['traffic'])
    scorable['total_score'] = sum([scorable['revenue_rank'], scorable['employees_rank'], scorable['funding_rank'], scorable['followers_rank'], scorable['traffic_rank']])
    scorable['fdo_score'] = sum([scorable['revenue_rank'], scorable['employees_rank'], 3 * scorable['funding_rank'], 2 * scorable['followers_rank'], 2 * scorable['traffic_rank']])
    for startup in startup_list:
        if scorable['ID'] == startup[id_type]:
            startup['{} Score'.format(study_name)] = scorable['total_score']
            startup['{} FDO Score'.format(study_name)] = scorable['fdo_score']
            for key in ['revenue_rank', 'employees_rank', 'funding_rank', 'followers_rank', 'traffic_rank']:
                startup[study_name + ' ' + key] = scorable[key]

ddmdata.writecsv(startup_list, '{}_scored.csv'.format(study_name))