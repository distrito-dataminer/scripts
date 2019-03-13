# Scripts

Scripts de uso geral para o Dataminer. 

### Usando Python

Para usar os scripts, você precisa ter o Python instalado. Baixe-o em https://www.python.org/downloads/. Quando instalar, selecione a opção "Add python to PATH". Cada script terá suas instruções de uso. Em geral, serão usados da seguinte forma:
1. Abra o prompt de comando (Win+R, escreva "cmd" e aperte enter)
2. Navegue até a pasta correta com o comando cd
3. Rode o script com o comando "python *script.py* *parâmetros adicionais*"

Instalando dependências

Quando um script listar dependências, instale-as antes de usá-lo com o comando "pip install *nome da dependência*" no prompt de comando.

## Scripts contidos neste repositório
### Categorizador e Revisor de Logos
*Categoriza logos em pastas de acordo com categorias, subcategorias e nomes contidos em um arquivo .csv. Exige um CSV de startups com as colunas 'Nome', 'Categoria', 'Subcategoria' e 'Site'. Os logos devem ter nomes de arquivo iguais ao nome da startup correspondente. O script ignora acentos, espaços e diferenças entre letras maiúsculas e minúsculas. Ao fim, ele também indica quais startups ficaram sem logo e vice versa, poupando o trabalho de revisão.*

**Input**: uma pasta de logos sem categorização  
**Output**: uma pasta de logos categorizados em subpastas, assim como uma lista de logos que não têm startup correspondente e startups do csv que ficaram sem logo.  
**Script**: categorizadorDeLogos.py  
**Dependências**: unidecode  

Uso:

    > python organizadorDeLogos.py [csv] [pasta com logos] [pasta destino]

Exemplo:

    > python organizadorDeLogos.py logos.csv "C:\logos" "C:\logos categorizados"

