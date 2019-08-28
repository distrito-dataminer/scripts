from utils import ddmdata, ddmsql, cleaner, sanity
from collections import OrderedDict

category_sub_category = ddmdata.idict_from_csv(
    'tables\\category_sub_category.csv')
category = ddmdata.idict_from_csv('tables\\category.csv')
customer_target = ddmdata.idict_from_csv('tables\\customer_target.csv')
legal_constituition = ddmdata.idict_from_csv('tables\\legal_constituition.csv')
sector_category = ddmdata.idict_from_csv('tables\\sector_category.csv')
sector = ddmdata.idict_from_csv('tables\\sector.csv')
startup_stage = ddmdata.idict_from_csv('tables\\startup_stage.csv')
sub_category = ddmdata.idict_from_csv('tables\\sub_category.csv')

startupList = ddmdata.readcsv('base.csv')

def createFormatted():
    formatted = OrderedDict()
    formatted['id'] = 'null'
    formatted['startup_stage_id'] = 'null'
    formatted['customer_target_id'] = 'null'
    formatted['legal_id'] = 'null'
    formatted['linkedin_url'] = 'null'
    formatted['crunchbase_url'] = 'null'
    formatted['facebook_url'] = 'null'
    formatted['legal_name'] = 'null'
    formatted['friendly_name'] = 'null'
    formatted['formatted_address'] = 'null'
    formatted['state'] = 'null'
    formatted['city'] = 'null'
    formatted['country'] = 'null'
    formatted['foundation_date'] = 'null'
    formatted['employee_quantity'] = 'null'
    formatted['emails'] = 'null'
    formatted['phone_number'] = 'null'
    formatted['company_description'] = ''
    formatted['logo_url'] = 'null'
    formatted['instagram_url'] = 'null'
    formatted['twitter_url'] = 'null'
    formatted['site_url'] = 'null'
    formatted['tags'] = ''
    formatted['is_foreign_entry'] = 1
    formatted['is_authenticated'] = 1
    formatted['is_active'] = 1
    return formatted

def createSectorization():
    sectorized = OrderedDict()
    sectorized['startup_id'] = 'null'
    sectorized['sector_id'] = 'null'
    sectorized['category_id'] = 'null'
    sectorized['sub_category_id'] = 'null'
    return sectorized

def formatList():
    
    formattedList = []

    for startup in startupList:
        formatted = createFormatted()
        if startup['Tirar?']:
            continue
        if startup['ID']:
            formatted['id'] = int(startup['ID'])
        if startup['Estágio da operação']:
            formatted['startup_stage_id'] = int(startup_stage[startup['Estágio da operação']])
        if startup['Público']:
            formatted['customer_target_id'] = int(customer_target[startup['Público'].strip()])
        if startup['Constituição Legal']:
            formatted['legal_id'] = int(legal_constituition[startup['Constituição Legal']])
        if startup['LinkedIn']:
            formatted['linkedin_url'] = startup['LinkedIn']
        if startup['Crunchbase']:
            formatted['crunchbase_url'] = startup['Crunchbase']
        if startup['Facebook']:
            formatted['facebook_url'] = startup['Facebook']
        if startup['Startup']:
            formatted['legal_name'] = startup['Startup']
            formatted['friendly_name'] = startup['Startup']
        if startup['Endereço']:
            formatted['formatted_address'] = startup['Endereço'].replace('"', r'\"')
        if startup['Estado']:
            formatted['state'] = startup['Estado']
        if startup['Cidade']:
            formatted['city'] = startup['Cidade']
        if startup['País']:
            formatted['country'] = startup['País']
        if startup['Ano de fundação']:
            formatted['foundation_date'] = startup['Ano de fundação'] + '-01-01'
        if startup['Funcionários LKD']:
            formatted['employee_quantity'] = int(startup['Funcionários LKD'].replace(',', ''))
        if startup['E-mail']:
            formatted['emails'] = startup['E-mail'].replace('"', r'\"')
        if startup['Telefone']:
            formatted['phone_number'] = startup['Telefone']
        if startup['Descrição']:
            formatted['company_description'] = startup['Descrição'].replace('"', r'\"')
        if startup['Logo LKD']:
            formatted['logo_url'] = startup['Logo LKD']
        if startup['Instagram']:
            formatted['instagram_url'] = startup['Instagram']
        if startup['Twitter']:
            formatted['twitter_url'] = startup['Twitter']
        if startup['Site']:
            formatted['site_url'] = startup['Site']
        if startup['Tags']:
            formatted['tags'] = startup['Tags'].replace('"', r'\"')
        formattedList.append(formatted)

    ddmdata.writecsv(formattedList, 'formattedOut.csv')

def sectorizeList():

    sectorizationList = []

    for startup in startupList:
        if startup['Tirar?']:
            continue
        setores = startup['Setor'].split(',')
        categorias = startup['Categoria'].split(',')
        subcategorias = startup['Subcategoria'].split(',')
        zipped = list(zip(setores,categorias,subcategorias))
        for setor, categoria, subcategoria in zipped:
            try:
                if setor:
                    sectorized = createSectorization()
                    sectorized['startup_id'] = startup['ID']
                    sectorized['sector_id'] = sector[setor]
                    if categoria:
                        sectorized['category_id'] = category[categoria]
                    if subcategoria:
                        sectorized['sub_category_id'] = sub_category[subcategoria]
                    sectorizationList.append(sectorized)
            except Exception as e:
                print(zipped)
                print(repr(e))
    
    ddmdata.writecsv(sectorizationList, 'sectorized_startups.csv')

sectorizeList()
