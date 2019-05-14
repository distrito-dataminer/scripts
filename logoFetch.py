#! python3
# logoFetch.py - Downloads images of logos from LinkedIn and saves them with the name of the company

import csv, requests, logging, sys, shutil, wget

logging.basicConfig(level=logging.DEBUG, format=' %(levelname)s - %(message)s')

file = sys.argv[1]
startupList = []
with open(file, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        startupList.append(row)

errors = []
nameErrors = []

for startup in startupList:
    name = startup['Startup']
    for c in r'\/?|:"*<>':
        name = name.replace(c, '')
    logging.debug('Getting logo for %s \n' % name)
    url = startup['Logo LKD']
    try:
        file = wget.download(url, out="C:\\test\\LKDlogos\\" + name + '.jpg')
        print(file)
    except Exception as e:
        print('Request failed.')
        print(repr(e))
    print('\n')
#     try:
#         res = requests.get(url, stream=True)
#     except:
#         logging.debug('Error when getting logo. Continuing')
#         errors.append(name)
#         continue
#     try:
#         imageFile = open("C:\\test\\LKDlogos\\" + name + '.png', 'wb')
#     except Exception as e:
#         logging.debug('Error when writing file. Check name?')
#         logging.debug('Exception: ' + str(e))
#         print
#         continue
#     shutil.copyfileobj(res.raw, imageFile)
# imageFile.close()

print("Done.")

if len(errors) > 0:
    print("The following logos had errors when fetching them:")
    for item in errors:
        print(item)

if len(nameErrors) > 0:
        print("The following logos had errors when writing the file:")
        for item in nameErrors:
            print(item)