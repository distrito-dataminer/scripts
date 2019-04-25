# Scripts

Scripts de uso geral para o Dataminer. 

### Usando o Python

Para usar os scripts, você precisa ter o Python instalado. Baixe-o em https://www.python.org/downloads/. Quando instalar, selecione a opção "Add python to PATH". Cada script terá suas instruções de uso. Em geral, serão usados da seguinte forma:
1. Abra o prompt de comando (Win+R, escreva "cmd" e aperte enter)
2. Navegue até a pasta correta com o comando cd
3. Rode o script com o comando "python *script.py* *parâmetros adicionais*"

Instalando dependências

Quando um script listar dependências, instale-as antes de usá-lo com o comando "pip install *nome da dependência*" no prompt de comando.

## Scripts contidos neste repositório
### Categorizador e Revisor de Logos
*Categoriza logos em pastas de acordo com categorias, subcategorias e nomes contidos em um arquivo .csv. Exige um CSV de startups com as colunas 'Nome', 'Categoria', 'Subcategoria' e 'Site'. Os logos devem ter nomes de arquivo iguais ao nome da startup correspondente. O script ignora acentos, espaços e diferenças entre letras maiúsculas e minúsculas. Ao fim, ele também indica quais startups ficaram sem logo e vice versa, poupando o trabalho de revisão.*

**Input**: Um csv e uma pasta de logos sem categorização  
**Output**: uma pasta de logos categorizados em subpastas, assim como uma lista de logos que não têm startup correspondente e startups do csv que ficaram sem logo.  
**Script**: categorizadorDeLogos.py  
**Dependências**: unidecode  

Uso:

    > python organizadorDeLogos.py [csv] [pasta com logos] [pasta destino]

Exemplo:

    > python organizadorDeLogos.py logos.csv "C:\logos" "C:\logos categorizados"

### Site Scraper
*Coleta informações relevantes sobre startups a partir de um arquivo .csv que contenha seus nome e sites. O script coleta CNPJ (que busca no site principal, página de Termos e página de Privacidade), LinkedIn, Facebook, Instagram, Twitter, e Crunchbase. O csv deve conter no mínimo as colunas 'Nome' e 'Site'. Ele também salva uma coluna 'Response' - qualquer valor diferente de 200 indica que houve algum problema na conexão com o site.*

**Input**: um csv contendo nomes e sites de startups.  
**Output**: um csv populado com informações coletadas sobre as startups a partir de seus sites.
**Script**: siteScraper.py  
**Dependências**: bs4, requests  

Uso:

    > python siteScraper.py [csv] [opcional: 'noreplace' - não substitui informações que já existam no csv]

Exemplo:

    > python organizadorDeLogos.py base.csv

### Link to LinkedIn
*Usando a API Google Custom Search, faz uma busca pelo LinkedIn de uma empresa a partir do formato [site:linkedin.com/company/ [site da startup]]. Retorna um csv com o LinkedIn preenchido e um indicativo da necessidade de revisão, pois os resultados nem sempre trazem a startup que se busca.*

**Input**: um csv contendo nomes e sites de startups.  
**Output**: um csv populado com URLs do LinkedIn correspondentes e indicativo da necessidade de revisão.
**Script**: linkToLinkedin.py
**Dependências**: google-api-python-client [**Atenção!** Este script usa uma API do Google e para isso é necessário configurar uma chave para uso. O Dataminer tem uma conta. Mais detalhes em console.developers.google.com]

Uso:

    > python linkToLinkedin.py [csv] [opcional: 'noreplace' - não substitui informações que já existam no csv]

Exemplo:

    > python linkToLinkedin.py startups.csv noreplace

### Data Cleaner
*Limpa dados de uma base de startups de acordo com os parâmetros do Distrito Dataminer.*
*Transforma URLs para o formato http:// sem / no final e sem www. Verifica se os CNPJs têm o número correto de dígitos (pois o Excel tende a comer 0s à esquerda) e tira os símbolos (-, ., /) deles.*
*Atualmente limpa Site, CNPJ, LinkedIn, Facebook, Instagram, Twitter e Crunchbase.*

**Input**: um csv contendo informações de startups.  
**Output**: um csv com as mesmas informações limpas
**Script**: dataCleaner.py
**Dependências**: 

Uso:

    > python dataCleaner.py [csv]

Exemplo:

    > python dataCleaner.py startups.csv 