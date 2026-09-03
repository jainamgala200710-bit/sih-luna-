# Geometric Verification Benchmark

## Overview
This document logs the evaluation of geometric verification techniques applied to classical feature matchers to filter out false correspondences (outliers).

## Evaluated Techniques
1. **RANSAC (Random Sample Consensus)**: 
   - Standard iterative method to estimate the homography matrix while classifying data into inliers and outliers.
2. **USAC / MAGSAC++**:
   - Advanced framework integrated into newer OpenCV versions (`cv2.USAC_MAGSAC`). Highly robust, fast, and does not strictly require a hard reprojection threshold, making it superior for varied resolution scales.

## Test Methodology
- Dataset: `pair_001` (Synthetic)
- Matcher: SIFT
- Preprocessing: None (raw synthetic input).
- Geometric Model: Homography (Perspective transformation).
- Reprojection Threshold: 3.0 pixels

## Results (Sample Run)
- **Initial Matches**: ~50-60 (using Lowe's Ratio Test = 0.75).
- **RANSAC Inliers**: ~35-40 matches.
- **Inlier Ratio**: ~70% (consistent with ground-truth evaluation in Phase 9).
- **Outlier Rejection Quality**: The visualizer (`OutlierVisualizer`) clearly shows crossing lines (false matches) painted in red, while geometrically consistent points are preserved in green. The computed Homography matrix aligns perfectly with the ground truth matrix.

## Next Steps
The geometric verification successfully eliminates outliers. The next phase (Phase 11) will focus on deep learning-based matching methods (SuperPoint, SuperGlue, LoFTR) to compare their raw inlier ratios against these classical baselines.
