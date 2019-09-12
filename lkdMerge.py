#! python3
# lkdMerge.py - Depois de rodar o bot de LinkedIn, anexa as informações de volta à planilha original
import csv, re, sys, os, shutil, ast
from utils import cleaner, ddmdata, enrich, privatekeys, sanity
from more_itertools import unique_everseen as unique

startup_csv = sys.argv[1]
lkd_csv = sys.argv[2]

startup_list = ddmdata.readcsv(startup_csv)
lkd_list = ddmdata.readcsv(lkd_csv)

startup_list = cleaner.clean(startup_list)

startup_list, address_list = ddmdata.lkd_merge(startup_list, lkd_list)

startup_list = cleaner.clean(startup_list)

ddmdata.writecsv(startup_list, '{}_lkd_merged.csv'.format(startup_csv.replace('.csv', '')))
ddmdata.writecsv(address_list, '{}_lkd_addresses.csv'.format(startup_csv.replace('.csv', '')))
