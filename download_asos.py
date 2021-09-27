import datetime
import os
import sys
import wx_config

state = wx_config.get_state_id()
station_asos = wx_config.get_station_id()
date_current = datetime.date.today()

fn_base = "https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?"
cmd = "network=%s_ASOS&stations=%s&year1=1980&month1=1&day1=1" % (state, station_asos)
cmd2 = "&year2=%d&month2=%d&day2=%d" % (date_current.year, date_current.month, date_current.day)

link = fn_base + cmd + cmd2
os.makedirs('./data', exist_ok = True)
cmd = 'wget -q -O data/%s_obs.txt "%s"' % (station_asos, link)
os.system(cmd)
