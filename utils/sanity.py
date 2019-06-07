#! python3

import sys
import csv
import re
from collections import OrderedDict

from more_itertools import unique_everseen as unique
from unidecode import unidecode
from jellyfish import levenshtein_distance as lev 

import ddmdata, cleaner

def sectlist(csvPath):
    l = ddmdata.readcsv(csvPath)
    cleanList = [(d['Setor'],d['Categoria'],d['Subcategoria']) for d in l]
    return cleanList

def catcheck(startupList, sectorList):
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
    with open('problems.txt', 'w') as problemfile:
        for item in list(unique(problems)):
            problemfile.write(str(item)+'\n')
    problemfile.close()

def dupeDetect(startupList):
    matchList = []
    for startup in startupList:
        site = startup['Site']
        if site == '':
            continue
        siteMatch = re.search(r'http:\/\/[^\.]*', site)
        for startup2 in startupList:
            if startup['ID'] == startup2['ID']:
                continue
            site2 = startup2['Site']
            if site2 == '':
                continue
            site2Match = re.search(r'http:\/\/[^\.]*', site2)
            if siteMatch == site2Match:
                matchList.append((site, site2)) 
    return matchList

def cemiterioCheck(startupList, cemiterio):
    for startup in startupList:
        site = startup['Site']
        if site == '':
            continue
        siteMatch = re.search(r'http:\/\/[^\.]*', site)
        for morta in cemiterio:
            sitemorta = morta['Site']
            if sitemorta == '':
                continue
            sitemortaMatch = re.search(r'http:\/\/[^\.]*', sitemorta)
            if siteMatch == sitemortaMatch:
                print('{} está na base de startups e também no cemitério.'.format(startup['Startup']))