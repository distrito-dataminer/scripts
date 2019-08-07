#! python3
# dataSearch.py - searches for startups containing terms in their tags or description.

from utils import ddmdata
from more_itertools import unique_everseen as unique

searchTerms = ['Big Data', 'Analytics']

startupList = ddmdata.readcsv('base.csv')

tagMatches = []
descriptionMatches = []
tndMatches = []
categoryMatches = []

for startup in startupList:
    for term in searchTerms:
        if term.lower() in startup['Tags'].lower():
            tagMatches.append(startup)
        if term.lower() in startup['Descrição'].lower():
            descriptionMatches.append(startup)
        if term.lower() in startup['Categoria'].lower() or term.lower() in startup['Subcategoria'].lower():
            categoryMatches.append(startup)

for match in tagMatches:
    if match in descriptionMatches:
        tndMatches.append(match)

tagMatches = list(unique(tagMatches))
descriptionMatches = list(unique(descriptionMatches))
tndMatches = list(unique(tndMatches))
categoryMatches = list(unique(categoryMatches))

print('Tag matches:')
print(len(tagMatches))
print('Description matches:')
print(len(descriptionMatches))
print('Tag and Description matches:')
print(len(tndMatches))
print('Category matches:')
print(len(categoryMatches))
    
ddmdata.writecsv(tagMatches, 'Matches_Tags.csv')
ddmdata.writecsv(descriptionMatches, 'Matches_Descrição.csv')
ddmdata.writecsv(tndMatches, 'Matches_Tags&Descrição.csv')
ddmdata.writecsv(categoryMatches, 'Matches_Categoria.csv')