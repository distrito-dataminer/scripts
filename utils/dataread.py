#! python3
# dataread.py - Limpa dados de um CSV para mantê-los no padrão Dataminer

import sys
import csv
import re
import pandas as pd
from collections import OrderedDict
from unidecode import unidecode

def read(file):
    xls_file = pd.ExcelFile(file)
    print(xls_file.sheet_names)
    print(xls_file.parse(xls_file.sheet_names[0]))