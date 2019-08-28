from utils import ddmdata

fbdata = ddmdata.readcsv('fbdata.csv')
fbresults = ddmdata.readcsv('fbresults.csv')
igresults = ddmdata.readcsv('igresults.csv')
ttresults = ddmdata.readcsv('ttresults.csv')

for startup in fbdata:
    for fbresult in fbresults:
        if startup['Facebook'] == fbresult['url']:
            startup['Likes FB'] = fbresult['likes']
            startup['Followers FB'] = fbresult['follows']
    for igresult in igresults:
        if startup['Instagram'] == igresult['instagram']:
            startup['Followers IG'] = igresult['followers']
    for ttresult in ttresults:
        if startup['Twitter'] == ttresult['Twitter']:
            startup['Followers TT'] = ttresult['followers']


ddmdata.writecsv(fbdata, 'fbdata_merged.csv')
