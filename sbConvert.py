#! python3
# sbConvert.py - Creates a list of startups from a StartupBase scraping result

import sys

from utils import ddmdata, cleaner

sb_list = ddmdata.readcsv(sys.argv[1])

startup_list = ddmdata.startups_from_startupbase(sb_list)

startup_list = cleaner.clean(startup_list)

ddmdata.writecsv(startup_list, 'startups_from_{}'.format(sys.argv[1]))