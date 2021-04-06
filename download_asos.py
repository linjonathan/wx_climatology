import datetime
import os
import sys

state = "KS" #sys.argv[1]
station_asos = "GLD" #sys.argv[2]
date_current = datetime.date.today()

fn_base = "https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?"
cmd = "network=%s_ASOS&stations=%s&year1=1980&month1=1&day1=1" % (state, station_asos)
cmd2 = "&year2=%d&month2=%d&day2=%d" % (date_current.year, date_current.month, date_current.day)

link = fn_base + cmd + cmd2

cmd = 'wget -q -O data/%s_obs.txt "%s"' % (station_asos, link)
os.system(cmd)
