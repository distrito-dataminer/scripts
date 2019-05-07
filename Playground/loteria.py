import random, pprint

participantes = {
 (7, 10, 14, 28, 59, 60): 'tiago',
 (1, 2, 3, 4, 5, 6): 'castro',
 (17, 22, 44, 46, 50, 58): 'fabricio',
 (4, 22, 30, 31, 44, 59): 'dani',
 (18, 22, 31, 32, 34, 58): 'vic',
 (3, 12, 27, 34, 42, 59): 'dudu',
 (5, 12, 14, 35, 43, 60): 'diego',
 (6, 12, 22, 24, 54, 55): 'felipe',
 (5, 23, 26, 30, 31, 53): 'mari',
 (11, 14, 27, 32, 51, 52): 'inae'
 }

winner = False
sorteios = 0

stats = {}

while winner == False:
    sorteios += 1
    resultado = []
    resultados = []
    bolinhas = 0
    while bolinhas < 6:
        bolinha = random.randint(1,60)
        if bolinha not in resultado:
            resultado.append(bolinha)
            bolinhas += 1
    resultado = sorted(resultado)
    resultado = tuple(resultado)
    if resultado in participantes.keys():
        winner = True
        print('ACHAMOS UM VENCEDOR!')
        print(participantes[resultado])
        print('Depois de {} sorteios!'.format(sorteios))
    if sorteios % 1000000 == 0:
        print(sorteios)
