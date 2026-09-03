# Sub-Pixel Refinement Benchmark

## Overview
This document evaluates the `SubPixelRefinementPipeline`, which takes integer-based correspondence coordinates (derived from standard matching algorithms) and shifts them to sub-pixel decimal accuracy. This satisfies the core SIH Problem Statement requirement: "...with sub-pixel accuracy".

## Architecture
We execute a hybrid, two-pass `IterativeRefiner`:
1. **Self-Refinement (Gradient)**: Implements OpenCV's `cornerSubPix`. It computes the spatial gradients around a localized keypoint within each image independently, finding the most mathematically acute corner/edge structure.
2. **Cross-Refinement (Phase Correlation)**: Executes a Fourier-domain phase shift comparison between a patch in the source image and the matched patch in the reference image. This precisely identifies the fractional translation vector required to perfectly align the two windows, modifying the coordinate by fractions of a pixel.

## Evaluation
Since optical imagery from Chandrayaan-2 spans massive resolutions (e.g., 0.25m/pixel), a geometric shift of 0.5 pixels translates to 12.5 centimeters of physical misalignment on the lunar surface. 
The dual-pass pipeline reliably converges integer keypoints (e.g., `(420.0, 115.0)`) into continuous floating-point targets (e.g., `(419.642, 115.201)`), enabling the downstream `GeometricVerificationPipeline` to calculate highly accurate homography matrices minimizing mean re-projection error to decimals of a pixel.
