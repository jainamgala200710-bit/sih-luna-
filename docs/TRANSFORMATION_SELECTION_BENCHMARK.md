# Transformation Selection Benchmark

## Overview
This document evaluates the `ModelValidationPipeline` designed to dynamically select the optimal mathematical structure for mapping source image pixels to reference image pixels. Rather than hard-coding a full Projective Homography (which can catastrophically over-fit and warp non-coplanar scenes when inliers are sparse), this engine evaluates multiple topologies and heuristically scores them.

## Geometric Models Supported
1. **Full Homography (Projective)**: 8 Degrees of Freedom (DoF). Best for planar surfaces or purely rotational camera motion. Highly susceptible to warping artifacts with low inlier counts.
2. **Affine**: 6 DoF. Allows for rotation, scaling, translation, and shear. Keeps parallel lines parallel.
3. **Partial Affine (Similarity)**: 4 DoF. Rotation, uniform scaling, and translation. Safest fallback model to prevent structural shearing on sparse data.

## Selection Logic
The `ModelSelector` executes a custom fitness heuristic:
`Score = (RMSE * Penalty) / log(Inliers + 1)`

- **RMSE**: Root Mean Square Error of the re-projection distance.
- **Penalty**: An escalating multiplier based on the model's Degrees of Freedom (1.20 for Partial Affine up to 1.40 for Homography) acting as an AIC (Akaike Information Criterion) equivalent to prevent overfitting.
- **Inliers**: Logarithmically dampens the score as consensus grows, rewarding models that safely fit larger numbers of robust points.

The model producing the lowest score is selected. The pipeline strictly defaults to rigid subsets if higher-DoF models lack sufficient mathematical support.
