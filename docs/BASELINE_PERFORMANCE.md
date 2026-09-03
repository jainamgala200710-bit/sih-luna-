# Baseline Feature Matching Performance

## Overview
This document logs the evaluation of classical feature matching algorithms (SIFT and ORB) applied to the Phase 4 synthetic lunar dataset.

## Evaluated Algorithms
1. **SIFT (Scale-Invariant Feature Transform)**:
   - *Strengths*: Highly robust to scale, rotation, and illumination differences.
   - *Weaknesses*: Computationally heavy, slower detection and description.
   - *Matcher*: FLANN-based KDTree Matcher with Lowe's Ratio Test (0.75).

2. **ORB (Oriented FAST and Rotated BRIEF)**:
   - *Strengths*: Extremely fast, rotation invariant, free of licensing/patents.
   - *Weaknesses*: Less robust to extreme scale and perspective changes compared to SIFT.
   - *Matcher*: Brute Force (Hamming Distance) with Ratio Test (0.8).

## Test Methodology
- Dataset: `pair_001` (Synthetic)
- Preprocessing: None (raw synthetic input).
- Evaluation Metric: Ground truth projection precision (matches within 3.0 pixel reprojection error based on the ground truth homography).

## Results (Sample Run)
- **SIFT**: High precision (>90% inlier ratio) under moderate perspective shifts. Usually finds 1000+ keypoints on 512x512 images.
- **ORB**: Good precision under pure rotation/scale, but degrades faster under perspective changes. Extracts keypoints significantly faster (usually cap at 5000 per parameters).

## Next Steps
These baselines demonstrate the necessity of robust outlier rejection. In Phase 10, Geometric Verification (RANSAC) will be introduced to automatically filter out the false positives without needing the ground truth matrices.
