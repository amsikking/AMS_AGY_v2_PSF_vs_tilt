# AMS_AGY_v2_psf_vs_tilt
Data showing how the (optical axis) psf from an AMS-AGY v2.0 objective changes with tilt
## Quick start:
- Download the whole repository (~400MB) and check out the 'data' folder. Each file is for either 'p' or 's' polarised light at a given tilt angle from 0-55deg.
- For estimates on transmission check out the included '.png' files, or run the associated '.py' files that generate the plots from the data folder.
- A photo of the setup is included
## Details:
- The data was collected with an AMS-AGY v2.0 objective (S/N 0001) paired with a Nikon 20x 0.75 air objective (MRD00205). The AMS-AGY objective was used in conjuction with a 200mm tube lens (Thorlabs TTL200MP) and sCMOS camera (PCO.edge42).
- A collimated 532nm laser source (Thorlabs CPS532) was aligned to the optic axis of the Nikon objective. The beam was expanded to fill the back aperture and 's' polarised light was rejected with a polarising cube (Thorlabs VA5-PBS251/M). Another polarizing cube (Thorlabs CCM1-PBS251/M) was then used with a half wave plate (Thorlabs WPMH10M-532) to calibrate a switching routine between 'p' and 's' polarisations (then used repeatedly for data collection with the CCM1 removed).
- 'p' polarised light refers to light that is polarized _in the plane_ of the table and therefore _in the plane of the tilt of the AMS-AGY objective_.
- The 'tilt' of the AMS-AGY objective (and corresponding microscope) was done 'by eye' using a digital protractor (see setup photo). It is estimated that the error on this operation was on the order of 1 degree. For each tilt angle the position of the AMS-AGY microscope (as a whole) was re-aligned to centre the laser focus back the the center of the camera chip (no other optics adjusted).
- A 20um piezo (Thorlabs PAS005) was used to take 'z-stacks' of the psf produced by the Nikon objective by moving a large stage (Thorlabs LNR50M) under the AMS-AGY objective (nominally aligned with the optic axis).
- For the acquisition details see the '.py' file in the data folder.

Note: the raw data was too large for the repository so a simple 'crop_roi.py' routine was applied (see data folder).
