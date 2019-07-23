import sys
from utils import ddmdata, cleaner, enrich
from func_timeout import func_timeout, FunctionTimedOut

ends = ddmdata.readcsv(sys.argv[1])
timeouts = 0
count = 0

for endereco in ends:
    if timeouts < 5:
        if count % 1000 == 0:
            ddmdata.writecsv(ends, 'ends_geocoded_partial_{}.csv'.format(str(count)))
        try:
            endereco = func_timeout(10, enrich.geocodeind, args=(endereco,))
        except FunctionTimedOut:
            timeouts += 1
            count += 1
            print('Timeout ao fazer o geocode de um endereço da {}'.format(endereco['Startup']))
        count += 1

ddmdata.writecsv(ends, 'ends_geocoded.csv')