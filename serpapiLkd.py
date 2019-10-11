from serpapi.google_search_results import GoogleSearchResults
from utils import ddmdata, privatekeys, enrich
import re

base = ddmdata.readcsv('base.csv')

base = enrich.serpapi_lkd(base)

ddmdata.writecsv(base, 'base_serpapi_lkds.csv')