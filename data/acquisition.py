import numpy as np
from tifffile import imread, imwrite
import pco_edge42_cl
import ni_PCIe_6738
import thorlabs_MDT694B

# hardware setup:
polarisation = 's'
tilt_deg = 55
camera_px_um = 6.5
mag = 200 / 9 # AMS_AGY_v2_EFL_mm / Thorlabs_TTL200MP_EFL_mm
Thorlabs_PAS005_range_um = 20
piezo_input_max_v = 10 # -> full range of Thorlabs PAS005

# calculate parameters:
AMS_AGY_v2_px_um = camera_px_um / mag
num_piezo_steps = Thorlabs_PAS005_range_um / AMS_AGY_v2_px_um # ~cubic voxels
frames = int(num_piezo_steps)
piezo_step_v = piezo_input_max_v / frames
piezo_voltages = np.arange(0, piezo_input_max_v, piezo_step_v)

# initialize hardware:
ao = ni_PCIe_6738.DAQ(num_channels=13, rate=4e5, verbose=False)
camera = pco_edge42_cl.Camera(verbose=True)
piezo = thorlabs_MDT694B.Controller('COM4', verbose=False)

# apply settings:
piezo.set_voltage(0)
camera.apply_settings(frames, 10000, 300, 300, 'binary+ASCII')

# set timing:
jitter_time_us = 30 # how much slop is needed between triggers? 30us?
jitter_px = max(ao.s2p(1e-6 * jitter_time_us), 1)
rolling_px = ao.s2p(1e-6 * camera.rolling_time_us)
exposure_px = ao.s2p(1e-6 * camera.exposure_us)
piezo_settle_px = ao.s2p(0.01) # slow down for piezo (approx time)
period_px = max(rolling_px, exposure_px) + jitter_px + piezo_settle_px

# calculate voltages:
voltage_series = []
for i in range(frames):
    volt_period = np.zeros((period_px, ao.num_channels), 'float64')
    volt_period[:rolling_px, 10] = 5 # (falling edge is time for laser on!)
    volt_period[:, 12] = piezo_voltages[i]
    voltage_series.append(volt_period)
voltages = np.concatenate(voltage_series, axis=0)

# get ready to acquire:
ao._write_voltages(voltages) # write voltages first to avoid delay
images = np.zeros( # allocate memory to pass in
    (camera.num_images, camera.height_px, camera.width_px), 'uint16')

# acquire:
for i in range(10):
    ao.play_voltages(block=False) # race condition!
    camera.record_to_memory( # -> waits for trigger
        allocated_memory=images, software_trigger=False)
    imwrite('%02ideg_%s_%02i.tif'%(tilt_deg, polarisation, i), images)

# tidy up:
ao.close()
camera.close()
piezo.set_voltage(75/2) # leave in center of range for next test
piezo.close()
