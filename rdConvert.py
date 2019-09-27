#! python3
# rdConvert.py - Converte um CSV de leads importado do RDStation para o formato da Base Distrito, para facilitar importação com o dataComplete.py
# Uso: rdConvert.py [csv do RD]

import sys
from utils import cleaner, ddmdata

rd_list = ddmdata.readcsv(sys.argv[1])
    
converted_list = cleaner.clean(ddmdata.rd_convert(rd_list))
    
ddmdata.writecsv(converted_list, sys.argv[1].replace('.csv', '') + '_rdConverted.csv')