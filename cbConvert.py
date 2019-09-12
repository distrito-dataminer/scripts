#! python3
# cbConvert.py - Creates a list of startups from a Crunchbase export result

import sys

from utils import ddmdata, cleaner

cb_list = ddmdata.readcsv(sys.argv[1])

startup_list = ddmdata.startups_from_crunchbase(cb_list)

startup_list = cleaner.clean(startup_list)

ddmdata.writecsv(startup_list, 'startups_from_{}'.format(sys.argv[1]))