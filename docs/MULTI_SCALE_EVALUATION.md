# Multi-Scale & Multi-Modal Evaluation

## Overview
This document logs the evaluation of the Coarse-to-Fine Multi-Scale matching pipeline alongside the Multi-Modal Histogram adapter, designed to resolve severe spatial resolution drops and sensor disparities (e.g., OHRC and LROC NAC).

## Evaluated Systems
1. **Pyramid Builder & Scale-Space Matcher**:
   - Generates iterative Gaussian blur decimations (base resolution / 2^i).
   - Extracts and matches features at each level (coarse to fine).
   - Aggregates matches by multiplying the spatial coordinates of coarse keypoints by their scale factor to reposition them onto the base image.

2. **Uncertainty Propagation**:
   - Matches found at lower resolutions carry inherently higher pixel uncertainty (e.g. level 2 matches have 4x the error bound). The propagator artificially increases their `distance` metric to deprioritize them below native-resolution matches during sorting.

3. **Multi-Modal Histogram Adapter**:
   - Employs empirical Cumulative Distribution Function (CDF) mapping to force one sensor's tonal range (e.g., LROC NAC) to match the other's (OHRC). This bridges the modality gap before feature extraction.

## Next Steps
In Phase 15, we will merge these sub-pipelines into a finalized Geometric Validation engine incorporating advanced structural uniform distribution algorithms (QuadTree) before proceeding to the final integration.
