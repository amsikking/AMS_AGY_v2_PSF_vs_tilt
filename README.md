# AMS_AGY_v2_psf_vs_tilt
Data showing how the psf from an AMS-AGY v2.0 objective changes with tilt
## Quick start:
- Download the whole repository (~400MB) and check out the 'data' folder. Each file is for either **'p' or 's' polarized light** at a given tilt angle **from 0-55deg**. Optionally run 'make_single_data_files.py' to view all the data in two 5D files.
- The data shows how the **image of a psf** produced by a Nikon objective **evolves as the AMS-AGY objective** (and associated microscope) **tilts** away from the original optical axis.
- For **transmission data** check out the included '.png' files (or run the associated '.py' files that generate the plots). The rudimentary **'max plot' shows a lower bound on transmission** based only on the average max for each set of psf's. The **'sum plot'** bins 3x3 at the focal plane (centered on max) and may offer a **better transmission estimate**.
- A photo of the setup is included
## Details:

- The data was collected with an AMS-AGY v2.0 objective (S/N 0001) paired with a Nikon 20x 0.75 air objective (MRD00205). The AMS-AGY objective was used in conjunction with a 200mm tube lens (Thorlabs TTL200MP) and sCMOS camera (PCO.edge42) combined into a single (large) assembly.
- A collimated 532nm laser source (Thorlabs CPS532) was aligned to the optic axis of the Nikon objective. The beam was expanded to fill the back aperture and 's' polarized light was rejected with a polarizing cube (Thorlabs VA5-PBS251/M). Another polarizing cube (Thorlabs CCM1-PBS251/M) was then used with a half wave plate (Thorlabs WPMH10M-532) to calibrate a switching routine between 'p' and 's' polarisations (then used repeatedly for data collection with the CCM1 removed).
- **'p' polarized light refers to light that is polarized in the plane of the table** and therefore in the plane of the tilt of the AMS-AGY objective.
- The 'tilt' of the AMS-AGY objective (and corresponding microscope) was done 'by eye' using a digital protractor (see setup photo). It is estimated that the error on this operation was on the order of 1 degree. For each tilt angle the position of the AMS-AGY microscope (as a whole) was realigned to put the laser focus back to the center of the camera chip (no other optics adjusted).
- A 20um piezo (Thorlabs PAS005) was used to take 'z-stacks' of the psf produced by the Nikon objective by moving a large stage (Thorlabs LNR50M) under the AMS-AGY objective (nominally aligned to its optic axis). For each acquisition the **AMS-AGY objective was moved from furthest separation** (about -10um from focus) **to closest separation** (about +10um beyond focus).
- For each tilt and polarisation the acquisition was repeated 10 times to help smooth out noise from table vibration and laser fluctuations in post processing. For acquisition details see the '.py' file in the data folder.

Note: the raw data was too large for the repository so a simple 'crop_roi.py' routine was applied (see data folder).
