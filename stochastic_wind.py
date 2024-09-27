from bufkit import ingest
import numpy as np
from bufkit import surface
from bufkit import sounding
import sys
import scipy.io

stn = str(sys.argv[1])
model = str(sys.argv[2])
bufr_file = ingest(stn, model)
utc_factor = int(sys.argv[3])

surface_data = surface(bufr_file)
sounding_data = sounding(bufr_file)

#  Pressure at top of mixed layer
mlp = np.array(surface_data.PRES)

# 10m zonal and meridional wind
w10u = np.array(surface_data['UWND'])
w10v = np.array(surface_data['VWND'])

# time-height cross sections of wind, pressure, and temperature
nP = len(sounding_data.PROFILE[0].PRES)
nT = len(sounding_data.PROFILE)
PRES = np.zeros((nT, nP))
TEMP = np.zeros((nT, nP))
SKNT = np.zeros((nT, nP))
DRCT = np.zeros((nT, nP))
for i in range(nT):
    PRES[i, :] = np.array(sounding_data.PROFILE[i].PRES)
    TEMP[i, :] = np.array(sounding_data.PROFILE[i].TMPC)
    SKNT[i, :] = np.array(sounding_data.PROFILE[i].SKNT)    
    DRCT[i, :] = np.array(sounding_data.PROFILE[i].DRCT)

TIME = np.array(surface_data['TIME'])
hrs = TIME.astype('datetime64[h]').astype(int) % 24

hrs_local = hrs + utc_factor
hrs_local[hrs_local < 0] = hrs_local[hrs_local < 0] + 24
midn_idx = np.argwhere(hrs_local == 0)[0:2].flatten()
scipy.io.savemat('data.mat', 
                 {'mlp': mlp, 'w10u': w10u, 'w10v': w10v, 'time': TIME,
                  'wth': SKNT, 'dth': DRCT, 'pth': PRES, 'tth': TEMP,
                  'midn_idx': midn_idx})

import os
cmd = "octave --no-gui run_stochastic_wind.m"
os.system(cmd)

f = open('stochastic_wind.txt')
wspds = np.array([float(x.rstrip('\n')) for x in f])
print(np.mean(wspds))
