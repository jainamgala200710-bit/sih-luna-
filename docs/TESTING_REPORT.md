# Edge Case Testing Report

## 1. Illumination Boundary Mapping
- **Objective**: Identify the maximum gradient variance tolerable before feature extraction failure.
- **Methodology**: Darkened reference synthetic datasets systematically using `test_extreme_illumination.py`.
- **Finding**: The SIFT matching topology mathematically breaks when the local gradient arrays invert (typically beyond a 90% artificial darkening threshold combined with spatial noise).
- **Behavior**: Instead of throwing C++ `Assertion failed (depth == CV_8U)` segfaults inside the RANSAC module, the custom `PipelineExhaustionError` wrapper intercepts the sub-4 match count and degrades gracefully via WebSocket JSON.

## 2. Scale Extremes Mapping
- **Objective**: Identify the absolute downscale limit of SIFT Gaussian Difference pyramids.
- **Methodology**: Shrunk an identical reference array to a 20x fractional scale mimicking the `OHRC` (0.25m) vs `TMC2` (5m) physical resolution reality in `test_scale_extremes.py`.
- **Finding**: At a 20x differential, the macroscopic structure is entirely lost in the sub-pixel blurring of the low-res image. $0$ Keypoint Nearest Neighbors were found.
- **Behavior**: Handled perfectly by `PipelineExhaustionError`.

## 3. High Frequency Noise
- **Objective**: Shatter the phase-correlation of the structural descriptors.
- **Methodology**: Obfuscated a primitive structural array entirely with Gaussian static in `test_high_noise.py`.
- **Finding**: The descriptors lock onto the static noise rather than the underlying structure, causing 100% false-positive matches which RANSAC rightfully rejects.
- **Behavior**: Returns $0$ Inliers, handled gracefully.
