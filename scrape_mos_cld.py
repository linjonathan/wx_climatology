from bs4 import BeautifulSoup
import datetime
import pickle
import requests
import os
import numpy as np
import sys
import wx_config

web_link = 'https://mesonet.agron.iastate.edu/mos/table.phtml?'
station = wx_config.get_station_id_4code()
start_dt = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
vnames = ['tmp', 'cld']
sys.setrecursionlimit(10000)

def get_mos_gfs_vname(dt, vname):
    # vname: 'cld', 'tmp'
    keys = 'station=%s&vname=%s&model=GFS&year=%d&month=%d&day=%02d' % (station, vname, dt.year, dt.month, dt.day)
    flink = '%s%s' % (web_link, keys)

    resp = requests.get(flink)
    txt = resp.text

    soup = BeautifulSoup(txt, 'lxml')
    table = soup.find(lambda tag: tag.name=='table')
    tables = soup.findChildren('table')
    mos_data = tables[0]
    rows = [x for x in mos_data.findChildren(['th', 'tr']) if len(x.findChildren('td')) > 0]

    mos_table = []

    for (i,row) in enumerate(rows[1:]):
        cells = row.findChildren('td')
        mos = []
        for (j, cell) in enumerate(cells[1:]):
            value = cell.string
            mos.append(value)
        mos_table.append(mos)

    return([dt] + [x[-1] for x in mos_table if x[-1] is not None])

def get_mos_nam_vname(dt, vname):
    # vname: 'cld', 'tmp'
    keys = 'station=%s&vname=%s&model=NAM&year=%d&month=%d&day=%02d' % (station, vname, dt.year, dt.month, dt.day)
    flink = '%s%s' % (web_link, keys)

    resp = requests.get(flink)
    txt = resp.text

    soup = BeautifulSoup(txt, 'lxml')
    table = soup.find(lambda tag: tag.name=='table')
    tables = soup.findChildren('table')
    mos_data = tables[0]
    rows = [x for x in mos_data.findChildren(['th', 'tr']) if len(x.findChildren('td')) > 0]

    mos_table = []

    for (i,row) in enumerate(rows[1:]):
        cells = row.findChildren('td')
        mos = []
        for (j, cell) in enumerate(cells[1:]):
            value = cell.string
            mos.append(value)
        mos_table.append(mos)

    return([dt] + [x[-1] for x in mos_table if x[-1] is not None][2:])

date_current = datetime.date.today()
yr = date_current.year
os.makedirs('./data', exist_ok = True)
for vname in vnames:
    gfs_mos_data = []
    nam_mos_data = []
    dt_base = datetime.datetime(yr, start_dt.month, start_dt.day, 0)
    dt_start = dt_base - datetime.timedelta(days=14)
    dt_end = dt_base + datetime.timedelta(days=21)

    dt = dt_start
    while dt <= dt_end and dt <= start_dt:
        gfs_mos_data.append(get_mos_gfs_vname(dt, vname))
        nam_mos_data.append(get_mos_nam_vname(dt, vname))
        dt = dt + datetime.timedelta(days=1)
        
    with open('data/%s_GFS_%s.data' % (station, vname), 'wb') as f:
        pickle.dump(gfs_mos_data, f)
        
    with open('data/%s_NAM_%s.data' % (station, vname), 'wb') as f:
        pickle.dump(nam_mos_data, f)
