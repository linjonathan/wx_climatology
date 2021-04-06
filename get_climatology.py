import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import plot_hist
import sys
from windrose import WindroseAxes
import matplotlib.cm as cm

station = 'GLD' #sys.argv[1]
f = open('data/%s.csv' % station)
data = csv.reader(f)

date_current = datetime.date.today()
date_start = date_current - datetime.timedelta(days = 7)
date_end = date_current + datetime.timedelta(days = 21)

keys = next(data);
pcp_idx = keys.index('PRCP')
Tmax_idx = keys.index('TMAX')
Tmin_idx = keys.index('TMIN')
wnd_idx = keys.index('WSF2')
wnddir_idx = keys.index('WDF2')

valid_data = []
for row in data:
    try:
        dt = datetime.datetime.strptime(row[2], '%Y-%m-%d')

        dt_start = datetime.datetime(dt.year, date_start.month, date_start.day, 0)
        dt_end = datetime.datetime(dt.year, date_end.month, date_end.day, 0)

        if dt >= dt_start and dt <= dt_end:
            pcp = float(row[pcp_idx])
            Tmax = float(row[Tmax_idx])
            Tmin = float(row[Tmin_idx])
            wnd = float(row[wnd_idx])
            wnd_dir = float(row[wnddir_idx])
            valid_data.append((dt, Tmax, Tmin, pcp, wnd, wnd_dir))
    except:
        pass

dts = np.asarray([x[0].strftime('%b-%d') for x in valid_data])
Tmax = np.asarray([x[1] for x in valid_data])
Tmin = np.asarray([x[2] for x in valid_data])
pcp = np.asarray([x[3] for x in valid_data])
wnd = [round(x[4]*0.868976) for x in valid_data]
wnd_dirs = [x[5] for x in valid_data]

plot_hist.hist_plot(Tmax, 2, '%s Max Temperature' % station, 'Mean = %f' % np.nanmean(Tmax))
plot_hist.hist_plot(Tmin, 2, '%s Min Temperature' % station, 'Mean = %f' % np.nanmean(Tmin))
plot_hist.cdf_plot(pcp, 0.02, '%s Precipitation' % station, 'Mean = %f' % np.nanmean(pcp))
plot_hist.hist_plot(wnd, 1, '%s 2-Minute Maximum Wind (knots)' % station, 'Mean = %f' % np.nanmean(wnd))

# %% wind rose
plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(9, 6.5))
ax = WindroseAxes.from_ax(theta_labels=["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"])
ax.bar(wnd_dirs, wnd, normed=True, nsector = 36, opening=1.0, bins=np.arange(5, 35, 5), edgecolor='white')
ax.set_legend(bbox_to_anchor=(-0.12, -0.1))
plt.title('%s Wind Rose' % station)
plt.savefig('fig/%s.png' % ('%s Wind Rose' % station))

"""
f = open('data/usl_mar2020_KAST.txt')
data = f.readlines()
keys = [line.rstrip('\n').split('\t') for line in data]
dates = np.asarray([datetime.datetime.strptime(x[0], '%m-%d-%Y') for x in keys])
uTmax = np.asarray([int(x[1][0:2]) for x in keys])
uTmin = np.asarray([int(x[2][0:2]) for x in keys])
uwnd = np.asarray([int(x[3][0:2]) for x in keys])
uPcp = np.asarray([float(x[4].rstrip('"')) for x in keys])

days = range(len(valid_data))
plt.figure(figsize=(12, 3))
plt.plot(days, uTmax - Tmax)
plt.scatter(np.asarray(days)[pcp > 0], np.full(np.sum(pcp > 0), np.max(uTmax - Tmax)+1), c='g')
plt.title('TMax: USL - Observed; Mean: %f' % np.mean(uTmax-Tmax))
plt.xlabel('Day'); plt.ylabel('Error (F)');
plt.xticks(days, dts); plt.grid(); plt.tight_layout()
plt.savefig('%s_USL_Tmax.png' % station)

plt.figure(figsize=(12, 3))
plt.plot(days, uTmin - Tmin)
plt.scatter(np.asarray(days)[pcp > 0], np.full(np.sum(pcp > 0), np.max(uTmin - Tmin)+1), c='g')
plt.title('TMin: USL - Observed; Mean: %f' % np.mean(uTmin-Tmin))
plt.xlabel('Day'); plt.ylabel('Error (F)');
plt.xticks(days, dts); plt.grid();  plt.tight_layout()
plt.savefig('%s_USL_Tmin.png' % station)

plt.figure(figsize=(12, 3))
plt.plot(days, uwnd - wnd)
plt.scatter(np.asarray(days)[pcp > 0], np.full(np.sum(pcp > 0), np.max(uwnd - wnd)+1), c='g')
plt.title('Wind: USL - Observed; Mean: %f' % np.mean(uwnd-wnd))
plt.xlabel('Day'); plt.ylabel('Error (kts)');
plt.xticks(days, dts); plt.grid();  plt.tight_layout()
plt.savefig('%s_USL_wind.png' % station)

plt.figure(figsize=(12, 3))
plt.plot(days, uPcp - pcp)
plt.title('Precipitation: USL - Observed; Mean: %f' % np.mean(uPcp-pcp))
plt.xlabel('Day'); plt.ylabel('Error (inches)');
plt.xticks(days, dts); plt.grid(); plt.tight_layout()
plt.savefig('%s_USL_pcp.png' % station)
"""
