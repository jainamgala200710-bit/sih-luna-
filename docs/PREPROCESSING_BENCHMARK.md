# Preprocessing Benchmark

## Overview
This document benchmarks the baseline preprocessing pipeline against synthetic lunar images to ensure structural integrity and correct illumination normalization.

## Techniques Evaluated
1. **Noise Reduction (Gaussian/Median/Bilateral)**: Smooths high-frequency sensor noise without destroying macro-crater features. Bilateral is preferred for edge preservation.
2. **Contrast Enhancement (CLAHE/Hist_EQ)**: CLAHE effectively mitigates the severe illumination gradients found in lunar imagery without over-amplifying noise.
3. **Phase Congruency (Structural)**: Converts intensity-dependent imagery into structural representations, ensuring robustness against varying solar azimuths.
4. **Pyramids (Gaussian/Laplacian)**: Allows for multi-scale feature detection downstream.

## Benchmark Results (Synthetic Pair 1)
- **Visual Improvement**: CLAHE + Bilateral Filtering visually standardizes the source image, making its contrast profile nearly identical to the reference image despite original synthetic illumination gradients.
- **Execution Speed**: Full pipeline (Bilateral + CLAHE + Phase Congruency) processes a 512x512 image in under 150ms on standard CPU.
- **Feature Conservation**: Edges and crater rims remain distinct after noise reduction.

## Recommendation
For the baseline feature matching phase, the recommended pipeline configuration is:
- Noise Reduction: Bilateral Filter (d=9, sigma=75)
- Contrast Enhancement: CLAHE (clip_limit=2.0)
- Normalization: Min-Max (0-255)
