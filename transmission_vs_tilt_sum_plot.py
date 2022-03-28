import numpy as np
from tifffile import imread, imwrite

tilts = np.arange(0, 60, 5) # microscope 3 tilt 0-55 degrees
reps = 10                   # acquisition number (for noise)
psf_radius_px = 1           # pixel radius to sum over

mean_sum_p, mean_sum_s = np.zeros((len(tilts))), np.zeros((len(tilts)))
stdv_sum_p, stdv_sum_s = np.zeros((len(tilts))), np.zeros((len(tilts)))

for t, tilt in enumerate(tilts):
    # get data:
    data_p = imread('data\%02ideg_p.tif'%tilt)
    data_s = imread('data\%02ideg_s.tif'%tilt)
    sum_p, sum_s = np.zeros(reps), np.zeros(reps)
    for r in range(reps): # find max intensity (focus) image for each repetition
        max_index_p = np.unravel_index(np.argmax(data_p[r]), data_p[r].shape)
        max_index_s = np.unravel_index(np.argmax(data_s[r]), data_s[r].shape)
        sum_p[r] = np.sum(data_p[
            r,
            max_index_p[0],
            max_index_p[1] - psf_radius_px:max_index_p[1] + psf_radius_px + 1,
            max_index_p[2] - psf_radius_px:max_index_p[2] + psf_radius_px + 1])
        sum_s[r] = np.sum(data_s[
            r,
            max_index_s[0],
            max_index_s[1] - psf_radius_px:max_index_s[1] + psf_radius_px + 1,
            max_index_s[2] - psf_radius_px:max_index_s[2] + psf_radius_px + 1])
    # average sum and stdev for plot:
    mean_sum_p[t], mean_sum_s[t] = np.average(sum_p), np.average(sum_s)
    stdv_sum_p[t], stdv_sum_s[t] = np.std(sum_p), np.std(sum_s)
    print('tilt = %02i, mean_sum_p = %04i, mean_sum_s = %04i'%(
          tilt, int(mean_sum_p[t]), int(mean_sum_s[t])))
    print('tilt = %02i, stdv_sum_p = %04i, stdv_sum_s = %04i'%(
          tilt, int(stdv_sum_p[t]), int(stdv_sum_s[t])))

mean_pct_p = 100 * mean_sum_p / max(mean_sum_p)
mean_pct_s = 100 * mean_sum_s / max(mean_sum_s)
mean_pct_p_s = (mean_pct_p + mean_pct_s) / 2

stdv_pct_p = 100 * stdv_sum_p / max(mean_sum_p)
stdv_pct_s = 100 * stdv_sum_s / max(mean_sum_s)
stdv_pct_p_s = (stdv_pct_p + stdv_pct_s) / 2

NA_limit_deg = np.rad2deg(np.arcsin(0.75))

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set_title('AMS-AGY v2.0 + Nikon 20x0.75 (MRD00205) @532nm')
ax.plot(tilts, mean_pct_p, label='p-polarised sum', linestyle='-.', color='b')
ax.plot(tilts, mean_pct_s, label='s-polarised sum', linestyle='--', color='g')
ax.errorbar(
    tilts, mean_pct_p_s, label='p+s sum', xerr=1, yerr=stdv_pct_p_s, color='r')
ax.axvline(x=NA_limit_deg, label='NA limit (0.75)', linestyle=':', color='k')
ax.set_xlabel('tilt angle (deg)')
ylabel = 'transmission estimate (%%) [psf_radius_px=%i]'%psf_radius_px
ax.set_ylabel(ylabel)
ax.legend()
plt.savefig('AMS_AGY_transmission_vs_tilt_sum_plot.png', dpi=200)
plt.show()
