import numpy as np
from tifffile import imread, imwrite

tilts = np.arange(0, 60, 5) # microscope 3 tilt 0-55 degrees
reps, z_px, h_px, w_px = 10, 67, 175, 75
all_data_p = np.zeros((reps, z_px, len(tilts), h_px, w_px), 'uint16') # 5D
all_data_s = np.zeros((reps, z_px, len(tilts), h_px, w_px), 'uint16') # 5D

for t, tilt in enumerate(tilts):
    data_p = imread('data\%02ideg_p.tif'%tilt)
    data_s = imread('data\%02ideg_s.tif'%tilt)
    all_data_p[:, :, t, :, :] = data_p
    all_data_s[:, :, t, :, :] = data_s

imwrite('all_data_p.tif', all_data_p, imagej=True, metadata={'axes': 'TZCYX'})
imwrite('all_data_s.tif', all_data_s, imagej=True, metadata={'axes': 'TZCYX'})
