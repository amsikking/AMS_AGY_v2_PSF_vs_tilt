import numpy as np
from tifffile import imread, imwrite

tilts = np.arange(0, 60, 5) # microscope 3 tilt 0-55 degrees
reps = 10                   # acquisition number (for noise)

mean_max_p, mean_max_s = np.zeros((len(tilts))), np.zeros((len(tilts)))
stdv_max_p, stdv_max_s = np.zeros((len(tilts))), np.zeros((len(tilts)))

for t, tilt in enumerate(tilts):
    # get data:
    data_p = imread('data\%02ideg_p.tif'%tilt)
    data_s = imread('data\%02ideg_s.tif'%tilt)
    max_p, max_s = np.zeros(reps), np.zeros(reps)
    for r in range(reps): # find max intensity for each repetition
        max_p[r] = np.max(data_p[r, :])
        max_s[r] = np.max(data_s[r, :])
    # average max and stdev for plot:
    mean_max_p[t], mean_max_s[t] = np.average(max_p), np.average(max_s)
    stdv_max_p[t], stdv_max_s[t] = np.std(max_p), np.std(max_s)
    print('tilt = %02i, mean_max_p = %04i, mean_max_s = %04i'%(
          tilt, int(mean_max_p[t]), int(mean_max_s[t])))
    print('tilt = %02i, stdv_max_p = %04i, stdv_max_s = %04i'%(
          tilt, int(stdv_max_p[t]), int(stdv_max_s[t])))

mean_pct_p = 100 * mean_max_p / max(mean_max_p)
mean_pct_s = 100 * mean_max_s / max(mean_max_s)
mean_pct_p_s = (mean_pct_p + mean_pct_s) / 2

stdv_pct_p = 100 * stdv_max_p / max(mean_max_p)
stdv_pct_s = 100 * stdv_max_s / max(mean_max_s)
stdv_pct_p_s = (stdv_pct_p + stdv_pct_s) / 2

NA_limit_deg = np.rad2deg(np.arcsin(0.75))

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set_title('AMS-AGY v2.0 + Nikon 20x0.75 (MRD00205) @532nm')
ax.plot(tilts, mean_pct_p, label='p-polarised max', linestyle='-.', color='b')
ax.plot(tilts, mean_pct_s, label='s-polarised max', linestyle='--', color='g')
ax.errorbar(
    tilts, mean_pct_p_s, label='p+s max', xerr=1, yerr=stdv_pct_p_s, color='r')
ax.axvline(x=NA_limit_deg, label='NA limit (0.75)', linestyle=':', color='k')
ax.set_xlabel('tilt angle (deg)')
ax.set_ylabel('transmission lower bound (%)')
ax.legend()
plt.savefig('AMS_AGY_transmission_vs_tilt_max_plot.png', dpi=200)
plt.show()
