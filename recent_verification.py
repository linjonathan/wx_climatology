import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle
import plot_hist
import wx_config
from bs4 import BeautifulSoup

station = wx_config.get_station_id()
f = open('data/%s_obs.txt' % station)
data = [x.split(',') for x in f.readlines()]

start_dt = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
recent_dt = start_dt - datetime.timedelta(days = 14)

keys = data[0]
pcp_idx = keys.index('precip_in')
Tmax_idx = keys.index('max_temp_f')
Tmin_idx = keys.index('min_temp_f')
wnd_idx = keys.index('max_wind_speed_kts')
wndavg_idx = keys.index('avg_wind_speed_kts')
wnddir_avg_idx = keys.index('avg_wind_drct')

valid_data = []
for row in data:
    try:
        dt = datetime.datetime.strptime(row[1], '%Y-%m-%d')
        pcp = float(row[pcp_idx])
        Tmax = float(row[Tmax_idx])
        Tmin = float(row[Tmin_idx])
        # 9/29/2021 (jzlin): Note, the data seem to have a units error for some stations. The variables
        # clearly indicate that the wind speed are in knots, but it appears that there is conversion 
        # errors in the units. So, we forcefully add the knots-to-mph factor to correct.
        wnd = float(row[wnd_idx]) / 0.869

        if (dt >= recent_dt) and (dt <= start_dt):
            valid_data.append((dt, Tmax, Tmin, pcp, wnd))
    except:
        pass

v_date = [x[0] for x in valid_data]
Tmax = np.asarray([x[1] for x in valid_data])
Tmin = np.asarray([x[2] for x in valid_data])
pcp = np.asarray([x[3] for x in valid_data])
wnds = np.asarray([x[4] for x in valid_data])

models = ['GFS', 'NAM']
max_mos = np.full((len(models), len(v_date)), np.nan)
min_mos = np.full((len(models), len(v_date)), np.nan)

for (m_idx, model) in enumerate(models):
    fn = open('data/K%s_%s.data' % (station, model), 'rb')
    mos = pickle.load(fn)
    fn = open('data/K%s_%s_tmp.data' % (station, model), 'rb')
    tmp_2m = pickle.load(fn)

    mos_dates = np.asarray([x[0] for x in mos])
    mos_mins = np.asarray([x[1][0] for x in mos])
    mos_maxs = np.asarray([x[1][1] for x in mos])

    mos_dates_2m = np.asarray([x[0] for x in tmp_2m])

    tmp2ms = [(np.asarray(x[3:12]).astype(int)) for x in tmp_2m]
    mos_max_2m = np.full(len(tmp2ms), np.nan)
    mos_min_2m = np.full(len(tmp2ms), np.nan)
    for i in range(len(tmp2ms)):
        if len(tmp2ms[i]) > 0:
            mos_max_2m[i] = np.max(tmp2ms[i])
            mos_min_2m[i] = np.min(tmp2ms[i])

    obs_max = np.full(len(v_date), np.nan)
    obs_min = np.full(len(v_date), np.nan)
    max_6z = np.full(len(v_date), False)
    min_6z = np.full(len(v_date), False)
    ver_dts = []

    for (i,x) in enumerate(v_date):
        idxs = np.argwhere(mos_dates == x).flatten()
        idxs2m = np.argwhere(mos_dates_2m == x).flatten()
        if len(idxs) > 0 and len(idxs2m) > 0:
            idx = idxs[0]; idx2m = idxs2m[0]
            max_mos[m_idx, i] = np.maximum(mos_maxs[idx], mos_max_2m[idx2m])
            min_mos[m_idx, i] = np.minimum(mos_mins[idx], mos_min_2m[idx2m])
            obs_max[i] = Tmax[i]
            obs_min[i] = Tmin[i]
            ver_dts.append(x.strftime('%b-%d'))
            if mos_maxs[idx] < mos_max_2m[idx2m]:
                max_6z[i] = True
            if mos_mins[idx] > mos_min_2m[idx2m]:
                min_6z[i] = True

days = range(len(valid_data))
tmp_range = range(int(np.minimum(np.nanmin(max_mos), np.nanmin(obs_max))),int(np.maximum(np.nanmax(max_mos), np.nanmax(obs_max)))+1, 2)
plt.figure(figsize=(10, 5))
cols = ['b', 'r']
for idx in range(len(models)):
    plt.plot(days, max_mos[idx, :], c=cols[idx], linewidth=len(models)-idx)
    plt.scatter(np.asarray(days)[max_6z], max_mos[idx, :][max_6z], c=cols[idx])
plt.plot(days, obs_max, 'kx')
plt.scatter(np.asarray(days)[pcp > 0], np.full(np.sum(pcp > 0), tmp_range[-1]+1), pcp[pcp> 0]*1000, c='g')
plt.title('TMax'); plt.legend(['GFS MOS', 'NAM MOS', 'Observed'])
plt.xlabel('Day'); plt.ylabel('Temperature (F)');
plt.xticks(days, ver_dts); plt.yticks(tmp_range);
plt.grid(); plt.tight_layout()
plt.savefig('fig/%s_recent_TMax.png' % station)
print('\tSaved fig/%s_recent_TMax.png' % station)

tmp_range = range(int(np.minimum(np.nanmin(min_mos), np.min(obs_min))),int(np.maximum(np.nanmax(min_mos), np.max(obs_min)))+1, 2)
plt.figure(figsize=(10, 5))
for idx in range(len(models)):
    plt.plot(days, min_mos[idx, :], c=cols[idx], linewidth=len(models)-idx)
    plt.scatter(np.asarray(days)[min_6z], min_mos[idx, :][min_6z], c=cols[idx])
plt.plot(days, obs_min, 'kx')
plt.scatter(np.asarray(days)[pcp > 0], np.full(np.sum(pcp > 0), tmp_range[-1]+1), pcp[pcp> 0]*1000, c='g')
plt.title('TMin'); plt.legend(['GFS MOS', 'NAM MOS', 'Observed'])
plt.xlabel('Day'); plt.ylabel('Temperature (F)');
plt.xticks(days, ver_dts); plt.yticks(tmp_range);
plt.grid(); plt.tight_layout()
plt.savefig('fig/%s_recent_TMin.png' % station)
print('\tSaved fig/%s_recent_TMin.png' % station)

plt.figure(figsize=(10, 5))
plt.plot(days, wnds, 'kx-')
plt.title('Observed Wind');
plt.xlabel('Day'); plt.ylabel('Wind (knots)');
plt.xticks(days, ver_dts);
plt.grid(); plt.tight_layout()
plt.savefig('fig/%s_recent_wnd.png' % station)
print('\tSaved fig/%s_recent_wnd.png' % station)
