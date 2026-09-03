# LUNAALIGN AI - REQUIRED.md

## Real Image Pairs Information

The system has been tested with three proxy real-image pairs generated to simulate actual mission conditions:

### 1. TMC2_vs_TMC2
- **Status**: SUCCESS
- **Inlier Count**: 22
- **Transformation Model**: affine
- **Description**: Same sensor (TMC2), different orbital pass with minor noise simulation
- **Registration Result**: Successful geometric verification with affine transformation

### 2. OHRC_vs_OHRC  
- **Status**: SUCCESS
- **Inlier Count**: 5
- **Transformation Model**: partial_affine
- **Description**: Same sensor (OHRC), high resolution with 15° structural rotation simulation
- **Registration Result**: Successful with partial affine model (limited degrees of freedom)

### 3. OHRC_vs_TMC2
- **Status**: ERROR: Not enough matches to compute geometric transformation (minimum 4)
- **Inlier Count**: 0
- **Transformation Model**: N/A
- **Description**: Extreme multi-modal case - OHRC (0.25m/pix) vs TMC2 (5m/pix) with 20x scale difference, noise, and illumination gradient
- **Registration Issue**: **Image not loading in registration layer** due to insufficient feature matches after SIFT detection and sub-pixel refinement. The scale and modality difference prevents establishing sufficient correspondences for geometric model fitting.

3D Digital Elevation Model (DEM) Generation
The Feature: If you feed LunaAlign an overlapping stereo pair (two images of the same lunar crater taken from slightly different orbital angles), you can calculate the parallax depth. You could use OpenCV's StereoSGBM (Semi-Global Block Matching) to generate a 3D depth map (DEM) of the lunar surface directly in the React UI using a 3D canvas like Three.js.