import numpy as np
from tifffile import imread, imwrite

tilts = np.arange(0, 60, 5)                 # microscope 3 tilt 0-55 degrees
reps = 10                                   # acquisition number (for noise)
ts_rows = 8                                 # ignore timestamp rows
z_px, h_px, w_px = 68, 300, 300             # raw data shape
roi_z_px, roi_h_px, roi_w_px = 67, 175, 75  # skip first image and crop

for t, tilt in enumerate(tilts):
    # make arrays to store all repetitions for a given tilt:
    all_reps_p = np.zeros((reps, z_px, h_px - ts_rows, w_px), 'uint16')
    all_reps_s = np.zeros((reps, z_px, h_px - ts_rows, w_px), 'uint16')
    for r in range(reps): # get the data:
        filename_p = '%02ideg_p_%02i.tif'%(tilt, r)
        filename_s = '%02ideg_s_%02i.tif'%(tilt, r)
        all_reps_p[r] = imread(filename_p)[:, ts_rows:, :]
        all_reps_s[r] = imread(filename_s)[:, ts_rows:, :]
        print('opened:', filename_p, filename_s)
    # crop using first repetition of p polarisation: (rough but good enough)
    max_index = np.unravel_index(np.argmax(all_reps_p[0]), all_reps_p[0].shape)
    # make arrays to store roi:
    all_reps_p_roi = np.zeros((reps, roi_z_px, roi_h_px, roi_w_px), 'uint16')
    all_reps_s_roi = np.zeros((reps, roi_z_px, roi_h_px, roi_w_px), 'uint16')
    # populate roi arrays with subset of data:
    all_reps_p_roi = all_reps_p[:,
                                1:, # ditch first image (noisy)
                                int(max_index[1] - roi_h_px / 2):
                                int(max_index[1] + roi_h_px / 2),
                                int(max_index[2] - roi_w_px / 2):
                                int(max_index[2] + roi_w_px / 2)]
    all_reps_s_roi = all_reps_s[:,
                                1:, # ditch first image (noisy)
                                int(max_index[1] - roi_h_px / 2):
                                int(max_index[1] + roi_h_px / 2),
                                int(max_index[2] - roi_w_px / 2):
                                int(max_index[2] + roi_w_px / 2)]
    # save:
    filename_p = '%02ideg_p.tif'%tilt
    filename_s = '%02ideg_s.tif'%tilt
    print('writing:', filename_p, filename_s)
    imwrite(filename_p, all_reps_p_roi, imagej=True, metadata={'axes': 'TZYX'})
    imwrite(filename_s, all_reps_s_roi, imagej=True, metadata={'axes': 'TZYX'})
