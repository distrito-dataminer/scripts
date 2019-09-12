#! python3
# lkdConvert.py - Creates a list of startups from a LinkedIn scraping result

import sys

from utils import ddmdata, cleaner

lkd_list = ddmdata.readcsv(sys.argv[1])

startup_list, address_list = ddmdata.startups_from_lkd(lkd_list)

startup_list = cleaner.clean(startup_list)

ddmdata.writecsv(startup_list, 'startups_from_{}'.format(sys.argv[1]))