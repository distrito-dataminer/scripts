#! python3
# dataSearch.py - searches for startups containing terms in their tags or description.

import sys
from utils import ddmdata
from more_itertools import unique_everseen as unique
from pprint import pprint
from collections import OrderedDict

startupList = ddmdata.readcsv(sys.argv[1])

if len(sys.argv) == 3:
    searchTerms = []
    searchTermsCsv = ddmdata.readcsv(sys.argv[2])
    for item in searchTermsCsv:
        searchTerms.append(item['Tags'])
else:
    searchTerms = ['Big Data', 'Analytics']

tagMatches = []
descriptionMatches = []
tndMatches = []
categoryMatches = []
setorMatches = []

tagDict = {}
descDict = {}
catDict = {}

for term in searchTerms:
    tagDict[term.lower()] = 0
    descDict[term.lower()] = 0
    catDict[term.lower()] = 0

for startup in startupList:
    if startup['Tirar?'] != '':
        continue
    matchCount = 0
    for term in searchTerms:
        if term.lower() in startup['Tags'].lower():
            tagMatches.append(startup)
            tagDict[term.lower()] += 1
            matchCount += 1
        if term.lower() in startup['Descrição'].lower():
            descriptionMatches.append(startup)
            descDict[term.lower()] += 1
            matchCount += 1
        if term.lower() in startup['Categoria'].lower() or term.lower() in startup['Subcategoria'].lower():
            categoryMatches.append(startup)
            catDict[term.lower()] += 1
            matchCount += 1
        if term.lower() in startup['Setor'].lower():
            setorMatches.append(startup)
            matchCount += 1
    startup['Match Count'] = matchCount

for match in tagMatches:
    if match in descriptionMatches:
        tndMatches.append(match)

tagMatches = list(unique(tagMatches))
descriptionMatches = list(unique(descriptionMatches))
tndMatches = list(unique(tndMatches))
categoryMatches = list(unique(categoryMatches))
setorMatches = list(unique(setorMatches))
mainMatches = list(unique(setorMatches + categoryMatches + tndMatches))
allMatches = list(unique(tagMatches + descriptionMatches + categoryMatches + setorMatches))

print('\n\nTag matches:')
print(len(tagMatches))
print('\n\nDescription matches:')
print(len(descriptionMatches))
print('\n\nTag and Description matches:')
print(len(tndMatches))
print('\n\nCategory matches:')
print(len(categoryMatches))
print('\n\nAll matches:')
print(len(allMatches))

tagDict = sorted(tagDict.items(), key=lambda kv: kv[1], reverse=True)
descDict = sorted(descDict.items(), key=lambda kv: kv[1], reverse=True)
catDict = sorted(catDict.items(), key=lambda kv: kv[1], reverse=True)

print('\n\nTag frequency:')
pprint(tagDict)
print('\n\nDescription frequency:')
pprint(descDict)
print('\n\nCategory frequency:')
pprint(catDict)
    
ddmdata.writecsv(tagMatches, 'Matches_Tags.csv')
ddmdata.writecsv(descriptionMatches, 'Matches_Descrição.csv')
ddmdata.writecsv(tndMatches, 'Matches_Tags&Descrição.csv')
ddmdata.writecsv(categoryMatches, 'Matches_Categoria.csv')
ddmdata.writecsv(setorMatches, 'Matches_Setor.csv')
ddmdata.writecsv(mainMatches, 'Matches_Main.csv')
ddmdata.writecsv(allMatches, 'Matches_All.csv')

