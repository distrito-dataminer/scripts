#! python3
# rdConvert.py - Converte um CSV de leads importado do RDStation para o formato da Base Distrito, para facilitar importação com o dataComplete.py
# Uso: rdConvert.py [csv do RD]

import sys
from utils import cleaner, ddmdata

conversionDict = {'Email': 'E-mail',
                  'Telefone': 'Telefone',
                  'Estado': 'Estado',
                  'Cidade': 'Cidade',
                  'Ano de Fundação': 'Ano de fundação',
                  'CNPJ': 'CNPJ',
                  'Constituição Legal': 'Constituição Legal',
                  'Descrição do Produto / Serviço': 'Descrição',
                  'Estágio atual': 'Estágio da operação',
                  'Faixa de faturamento anual': 'Faturamento Presumido',
                  'LinkedIn Company Page da Startup': 'LinkedIn',
                  'Modelo de negócios': 'Modelo de negócio',
                  'Modelo do Público': 'Público',
                  'Nome Completo dos Fundadores': 'Founders',
                  'Número de funcionários da sua empresa': 'Faixa # de funcionários',
                  'Segmento da Startup': 'Setor',
                  'Site da Startup': 'Site',
                  'Startup': 'Startup'}

rdList = ddmdata.readcsv(sys.argv[1])
convertedList = []

for startup in rdList:
    convertedStartup = {}
    for key in startup:
        if key in conversionDict:
            convertedStartup[conversionDict[key]] = startup[key]
    convertedList.append(convertedStartup)
    
convertedList = cleaner.clean(convertedList)
    
ddmdata.writecsv(convertedList, sys.argv[1].replace('.csv', '') + '_rdConverted.csv')