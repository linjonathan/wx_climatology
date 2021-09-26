from bs4 import BeautifulSoup
import datetime
import pickle
import requests
import numpy as np
import sys

web_link = 'https://mesonet.agron.iastate.edu/mos/table.phtml?'
station = 'K' + sys.argv[1]
model = sys.argv[2]
start_dt = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

def get_mos_gfs(dt):
    keys = 'station=%s&vname=n_x&model=GFS&year=%d&month=%d&day=%02d' % (station, dt.year, dt.month, dt.day)
    flink = '%s%s' % (web_link, keys)

    resp = requests.get(flink)
    txt = resp.text

    soup = BeautifulSoup(txt, 'lxml')
    table = soup.find(lambda tag: tag.name=='table')
    tables = soup.findChildren('table')
    mos_data = tables[0]
    rows = [x for x in mos_data.findChildren(['th', 'tr']) if len(x.findChildren('td')) > 0]
    mos_table = np.zeros((9, 14))

    for (i,row) in enumerate(rows[1:]):
        cells = row.findChildren('td')
        for (j, cell) in enumerate(cells[1:]):
            value = cell.string
            mos_table[i,j] = value

    date_keys = [np.nan]*14
    for i in range(14):
        date_keys[i] = dt - datetime.timedelta(hours=6)*(14-i)

    fcsts = mos_table[-3:-1, -1]
    mins = fcsts[0]
    maxs = fcsts[1]
    return(mins, maxs)

def get_mos_nam(dt):
    keys = 'station=%s&vname=n_x&model=NAM&year=%d&month=%d&day=%02d' % (station, dt.year, dt.month, dt.day)
    flink = '%s%s' % (web_link, keys)

    resp = requests.get(flink)
    txt = resp.text

    soup = BeautifulSoup(txt, 'lxml')
    table = soup.find(lambda tag: tag.name=='table')
    tables = soup.findChildren('table')
    mos_data = tables[0]
    rows = [x for x in mos_data.findChildren(['th', 'tr']) if len(x.findChildren('td')) > 0]
    mos_table = np.zeros((9, 7))

    for (i,row) in enumerate(rows[1:]):
        cells = row.findChildren('td')
        for (j, cell) in enumerate(cells[1:]):
            value = cell.string
            mos_table[i,j] = value

    date_keys = [np.nan]*7
    for i in range(7):
        date_keys[i] = dt - datetime.timedelta(hours=6)*(14-i)

    fcsts = mos_table[-3:-1, -1]
    mins = fcsts[0]
    maxs = fcsts[1]
    return(mins, maxs)

mos_data = []

for yr in range(2021, start_dt.year+1):
    dt_base = datetime.datetime(yr, start_dt.month, start_dt.day, 0)
    dt_start = dt_base - datetime.timedelta(days=14)
    dt_end = dt_base + datetime.timedelta(days=21)

    dt = dt_start
    while dt <= dt_end and dt < start_dt:
        if model == 'GFS':
            mos_data.append((dt, get_mos_gfs(dt)))
        elif model == 'NAM':
            mos_data.append((dt, get_mos_nam(dt)))

        dt = dt + datetime.timedelta(days=1)

with open('data/%s_%s.data' % (station, model), 'wb') as f:
    pickle.dump(mos_data, f)
