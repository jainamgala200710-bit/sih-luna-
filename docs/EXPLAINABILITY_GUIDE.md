# Explainability Guide

## Overview
The `explainability` module provides a comprehensive suite of diagnostic and visual tools designed to answer a single question: *Why did the algorithm pair these two pixels together?*

By generating human-readable "Dossiers" for specific points, we build scientific trust in the automated Registration Pipeline.

## Components

### 1. Match Information Panel
Extracts metadata straight from the descriptor algorithms.
- **Coordinates**: The exact sub-pixel source vs reference locations.
- **Scale Ratio**: Displays how much the multi-scale tracker had to warp the patch size to find a structural match.
- **Angle Difference**: Displays rotational invariance adjustments.

### 2. Feature Similarity Visualizer
A mathematical distance heuristic is useless if it doesn't align with human structural perception. The `FeatureSimilarityVisualizer` physically extracts the pixel boundaries around the match, scales them up 4x, and tiles them side-by-side. If the algorithm matched a crater to a crater, the images will visually prove it.

### 3. Geometric Consistency Checker
Takes the global transformation (e.g. Homography) computed by RANSAC and isolates the match. It executes the projection algorithm in a sandbox and calculates the isolated Euclidean error, proving mathematically if the point is an Inlier or an Outlier.

### 4. Refinement Visualizer
Details the specific Phase Correlation sub-pixel shift. Shows exactly how many fractions of a pixel the algorithm slid the coordinate to achieve perfect patch alignment.

### 5. Uncertainty Visualizer
Scale-space extrema (like SIFT keypoints) are extracted at varying blur layers (octaves). A match found at a high blur layer inherently possesses spatial uncertainty when mapped back to the raw high-resolution image. This visualizer renders a 1-Sigma radial heat boundary, visually demonstrating the geometric tolerance bounds of the coordinate.
