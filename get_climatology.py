import datetime
import numpy as np
import plot_hist
from windrose import WindroseAxes
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import os
import wx_config

station = wx_config.get_station_id()
f = open('data/%s_obs.txt' % station)
data = [x.split(',') for x in f.readlines()]

date_current = datetime.date.today()
date_start = date_current - datetime.timedelta(days = 7)
date_end = date_current + datetime.timedelta(days = 21)

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

        dt_start = datetime.datetime(dt.year, date_start.month, date_start.day, 0)
        dt_end = datetime.datetime(dt.year, date_end.month, date_end.day, 0)

        if dt >= dt_start and dt <= dt_end:
            pcp = float(row[pcp_idx])
            Tmax = float(row[Tmax_idx])
            Tmin = float(row[Tmin_idx])
            # 9/29/2021 (jzlin): Note, the data seem to have a units error for some stations. The variables
            # clearly indicate that the wind speed are in knots, but it appears that there is conversion 
            # errors in the units. So, we forcefully add the knots-to-mph factor to correct.
            wnd = float(row[wnd_idx]) / 0.8689
            if wnd == 0:
                wnd = np.nan
            wndavg = float(row[wndavg_idx])
            wnddiravg = float(row[wnddir_avg_idx])
            valid_data.append((dt, Tmax, Tmin, pcp, wnd, wndavg, wnddiravg))
    except:
        pass

dts = np.asarray([x[0].strftime('%b-%d') for x in valid_data])
Tmax = np.asarray([x[1] for x in valid_data])
Tmin = np.asarray([x[2] for x in valid_data])
pcp = np.asarray([x[3] for x in valid_data])
wnd = [x[4] for x in valid_data]
avgwnd = [x[5] for x in valid_data]
avgwnd_dirs = [x[6] for x in valid_data]

plot_hist.hist_plot(Tmax, 2, '%s Max Temperature' % station, 'Mean = %f' % np.nanmean(Tmax))
plot_hist.hist_plot(Tmin, 2, '%s Min Temperature' % station, 'Mean = %f' % np.nanmean(Tmin))
plot_hist.cdf_plot(pcp, 0.02, '%s Precipitation' % station, 'Mean = %f' % np.nanmean(pcp))
plot_hist.hist_plot(wnd, 1, '%s 2-Minute Maximum Wind (knots)' % station, 'Mean = %f' % np.nanmean(wnd))

# %% wind rose
plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(9, 6.5))
ax = WindroseAxes.from_ax(theta_labels=["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"])
w_max = np.nanquantile(avgwnd, 0.99) + 5
ax.bar(avgwnd_dirs, avgwnd, normed=True, nsector = 36, opening=1.0, bins=np.arange(5, w_max, 5), edgecolor='white')
ax.set_legend(bbox_to_anchor=(-0.12, -0.1))
plt.title('%s Average-Wind Wind-Rose' % station)
os.makedirs('./fig', exist_ok = True)
plt.savefig('fig/%s.png' % ('%s Wind Rose' % station))
