import itertools
from more_itertools import unique_everseen as unique
from utils import ddmdata
import sys

ends = ddmdata.readcsv(sys.argv[1])
weird_ends = []

for end in ends:
    try:
        if 'Confiança' in end and int(end['Confiança']) <= 7:
            ends.remove(end)
    except:
        continue

for end1, end2 in itertools.permutations(ends, 2):
    if end1['Startup'] == end2['Startup'] and end1['Startup'] != '':
        if end1['País'] == 'BR' and end2['País'] != 'BR':
            if end2 in ends:
                ends.remove(end2)

for end1, end2 in itertools.permutations(ends, 2):
    if end1['Startup'] == end2['Startup'] and end1['Startup'] != '':
        if end1['Estado'] in ['DF', 'GO'] and end2['Estado'] not in ['DF', 'GO']:
            if end2 in ends:
                ends.remove(end2)

for end1, end2 in itertools.permutations(ends, 2):
    if end1['Startup'] == end2['Startup'] and end1['Startup'] != '':
        if end1['End. Fiscal'] not in ['', 'FALSE'] and end2['End. Fiscal'] in ['', 'FALSE']:
            if end2 in ends:
                ends.remove(end2)

for end1, end2 in itertools.permutations(ends, 2):
    if end1['Startup'] == end2['Startup']:
        if end1['End. Fiscal'] == 'HQ LKD' and end2['End. Fiscal'] != 'HQ LKD':
            if end2 in ends:
                ends.remove(end2)

for end1, end2 in itertools.combinations(ends, 2):
    if end1['Startup'] == end2['Startup']:
        if end1['Latitude'] == end2['Latitude'] or end1['CEP'] == end2['CEP']:
            if end2 in ends:
                ends.remove(end2)

for end1, end2 in itertools.combinations(ends, 2):
    if end1['Startup'] == end2['Startup']:
        if end2 in ends:
            ends.remove(end2)

print(len(ends))

ddmdata.writecsv(ends, 'ends_filtered.csv')