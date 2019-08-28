#! python3

import sys
import csv
import re
from collections import OrderedDict

from more_itertools import unique_everseen as unique
from unidecode import unidecode
from jellyfish import levenshtein_distance as lev 

from utils import ddmdata, cleaner

def sector_list(csvPath):
    l = ddmdata.readcsv(csvPath)
    cleanList = [(d['Setor'],d['Categoria'],d['Subcategoria']) for d in l]
    return cleanList

def category_check(startupList, sectorList):
    print("Startups com disparidade entre número de setores, categorias e subcategorias:")
    problems = []
    for startup in startupList:
        if startup['Subcategoria']:
            if not len(startup['Categoria'].split(',')) == len(startup['Subcategoria'].split(',')) == len(startup['Setor'].split(',')):
                print(startup['Startup'])
    for startup in startupList:
        if startup['Setor']:
            setores = startup['Setor'].split(',')
            categorias = startup['Categoria'].split(',')
            subcategorias = startup['Subcategoria'].split(',')
            zipped = list(zip(setores,categorias,subcategorias))
            for item in zipped:
                if item not in sectorList:
                    problems.append(item)
    if len(problems) > 0:
        with open('problems.txt', 'w') as problemfile:
            for item in list(unique(problems)):
                problemfile.write(str(item)+'\n')
        problemfile.close()

def dupe_detect(startupList):
    dupeList = []
    for startup in startupList:
        startup['Checked'] = True
        if startup['Site'] == '':
            continue
        for startup2 in startupList:
            if 'Checked' in startup2:
                continue
            if startup['ID'] == startup2['ID']:
                continue
            if startup2['Site'] == '':
                continue
            if startup['Site'] == startup2['Site']:
                dupeList.append(startup2)
                #matchList.append((startup['Site'], startup2['Site'])) 
    for dupe in dupeList:
        del dupe[-1]
    return dupeList

def cemiterio_check(startupList, cemiterio):
    for startup in startupList:
        site = startup['Site']
        if site == '':
            continue
        for morta in cemiterio:
            sitemorta = morta['Site']
            if sitemorta == '':
                continue
            if site == sitemorta:
                print('{} está na base de startups e também no cemitério.'.format(startup['Startup']))