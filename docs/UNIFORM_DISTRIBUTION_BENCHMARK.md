# Uniform Spatial Distribution Benchmark

## Overview
This document evaluates the `UniformDistributionPipeline`, which enforces an explicit, uniform spatial distribution of geometric correspondences. This explicitly solves a primary constraint of the SIH Problem Statement (maintaining uniform distribution of correspondence points across the images).

## Algorithm Details
- **Grid Division**: The image is mapped onto a uniform $M \times N$ cell matrix.
- **Adaptive Non-Maximum Suppression (ANMS)**: Inside each localized grid cell, matches are dynamically thresholded up to a `max_per_cell` capacity. Matches are inherently sorted by descriptor `distance` prior to suppression, ensuring that only the highest-confidence points survive within that localized region.

## Evaluated Metrics
1. **Coverage %**: The percentage of physical grid cells containing at least one valid correspondence.
2. **Spatial Entropy**: Quantifies the evenness of the distribution. A perfectly balanced distribution yields maximum entropy, whereas clustered distributions (e.g. all points in a single cell) collapse entropy toward 0.

## Test Results
By post-processing the output of our matchers through the `UniformDistributionPipeline`, we guarantee an explicit cap on local clustering. The visualizer explicitly generates `grid_vis.png` which overlays the suppression bounds over the extracted coordinates, visualizing the algorithm's effect on enforcing full image coverage without risking algorithmic skew during homography calculation.
