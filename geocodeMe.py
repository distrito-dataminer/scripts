import sys
from utils import ddmdata, cleaner, enrich
from func_timeout import func_timeout, FunctionTimedOut
from time import sleep

ends = ddmdata.readcsv(sys.argv[1])
new_addresses = []
timeouts = 0
count = 0

for endereco in ends:
    if timeouts < 5:
        if count % 1000 == 0 and count != 0:
            ddmdata.writecsv(new_addresses, sys.argv[1].replace('.csv', '') + '_geocoded_partial_{}.csv'.format(str(count)))
        if count % 3 == 0:
            sleep(1)
        try:
            new_address = func_timeout(10, enrich.geocode_individual, args=(endereco,))
            new_addresses.append(new_address)
        except FunctionTimedOut:
            timeouts += 1
            count += 1
            print('Timeout ao fazer o geocode de um endereço da {}'.format(endereco['Startup']))
        count += 1

ddmdata.writecsv(new_addresses, sys.argv[1].replace('.csv', '') + '_geocoded.csv')