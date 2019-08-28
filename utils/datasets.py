# datasets.py
# Dicionários, listas e demais dados utilizados em scripts diversos do Dataminer


siglas = {
    "acre": "AC",
    "alagoas": "AL",
    "amapa": "AP",
    "amazonas": "AM",
    "bahia": "BA",
    "ceara": "CE",
    "distritofederal": "DF",
    "espiritosanto": "ES",
    "goias": "GO",
    "maranhao": "MA",
    "matogrosso": "MT",
    "matogrossodosul": "MS",
    "minasgerais": "MG",
    "para": "PA",
    "paraiba": "PB",
    "parana": "PR",
    "pernambuco": "PE",
    "piaui": "PI",
    "riodejaneiro": "RJ",
    "riograndedonorte": "RN",
    "riograndedosul": "RS",
    "rondonia": "RO",
    "roraima": "RR",
    "santacatarina": "SC",
    "saopaulo": "SP",
    "sergipe": "SE",
    "tocantins": "TO",
    "ac": "AC",
    "al": "AL",
    "ap": "AP",
    "am": "AM",
    "ba": "BA",
    "ce": "CE",
    "df": "DF",
    "es": "ES",
    "go": "GO",
    "ma": "MA",
    "mt": "MT",
    "ms": "MS",
    "mg": "MG",
    "pa": "PA",
    "pb": "PB",
    "pr": "PR",
    "pe": "PE",
    "pi": "PI",
    "rj": "RJ",
    "rn": "RN",
    "rs": "RS",
    "ro": "RO",
    "rr": "RR",
    "sc": "SC",
    "sp": "SP",
    "se": "SE",
    "to": "TO"
}

cidades = {
    'saopaulo': 'São Paulo',
    'sp': 'São Paulo',
    'riodejaneiro': 'Rio de Janeiro',
    'rj': 'Rio de Janeiro',
    'belohorizonte': 'Belo Horizonte',
    'bh': 'Belo Horizonte',
    'brasilia': 'Brasília',
    'florianopolis': 'Florianópolis',
    'floripa': 'Florianópolis',
    'sampa': 'São Paulo',
    'saopaulosp': 'São Paulo',
    'niteroi': 'Niterói',
    'saoleopoldo': 'São Leopoldo',
    'portoalegre': 'Porto Alegre',
    'saocarlos': 'São Carlos',
    'portoalegrers': 'Porto Alegre',
    'saocaetano': 'São Caetano',
    'saocaetanodosul': 'São Caetano do Sul',
    'saojosedoscampos': 'São José dos Campos',
    'maringa': 'Maringá',
    'goiania': 'Goiânia',
    'curitiba': 'Curitiba',
    'chapeco': 'Chapecó',
    'vitoria': 'Vitória',
    'joinville': 'Joinville'
}

invalidsites = [
    'http://facebook.com', 'http://linkedin.com', 'http://google.com', 'http://pipe.social'
]

invalidFacebook = ['http://facebook.com/sharer', 'http://facebook.com/share']

invalidTwitter = ['http://twitter.com/share']

invalidEmail = ['@sentry.wixpress.com', '@example', '@exemplo', '@sentry.io', 'communities-translations', 'ajax-loader', 'communities-blog-viewer-app', 'suporte@contabilizei.com.br']