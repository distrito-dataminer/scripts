#! python3


def ndp(startupList):
    for startup in startupList:
        score = 0
        if startup['Nome'] and startup['Site'] and startup['Fonte']:
            score += 5
        if startup['CNPJ']:
            score += 5
        if startup['Response']:
            score += 1
        if startup['LinkedIn']:
            score += 3
        if startup['Logo LKD']:
            score += 3
        if startup['Descrição']:
            score += 3
        if startup['Ano de fundação']:
            score += 3
        if startup['Cidade'] and startup['Estado'] and startup['País']:
            score += 3
        if startup['Funcionários LKD']:
            score += 3
        if startup['Faixa # de funcionários']:
            score += 1
        if startup['Setor']:
            score += 5
        if startup['Categoria']:
            score += 5
        if startup['Público']:
            score += 3
        if startup['Tags']:
            taglist = startup['Tags'].split(',')
            if len(taglist) >= 5:
                score += 2
            elif len(taglist) >= 10:
                score += 3
            elif len(taglist) >= 15:
                score += 4
        if startup['Crunchbase']:
            score += 2
        if startup['Facebook']:
            score += 1
        if startup['Instagram']:
            score += 1
        if startup['Twitter']:
            score += 1
        if startup['Faturamento Presumido']:
            score += 4
        # TODO: Outros dados TU - Score 2
        if startup['E-mail']:
            score += 2
        if startup['Telefone'] and startup['Endereço']:
            score += 1
        if startup['Founders']:
            score += 2
        if startup['Modelo de negócio']:
            score += 3
        if startup['Logo Estudo']:
            score += 4
        if startup['Acelerada por'] or startup['Investida por'] or startup['Incubada por'] or startup['Hub de inovação']:
            score += 5
        if startup['CAC'] or startup['LTV'] or startup['Ticket Médio'] or startup['Churn Rate']                               \
                or startup['MRR'] or startup['GMV'] or startup['Visitantes no site por mês'] or startup['Taxa de Conversão']  \
                or startup['Downloads do App'] or startup['Usuários ativos'] or startup['Crescimento Receita Trimestral']     \
                or startup['Receita mensal atual'] or startup['Despesa mensal atual']:
            score += 5
        startup['NDP'] = round((score / 80) * 100)
    return startupList
