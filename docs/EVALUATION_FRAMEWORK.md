# Evaluation & Benchmarking Framework

## Overview
This document outlines the architecture of the comprehensive benchmark suite developed to ensure that every algorithmic modification mathematically pushes the system toward achieving sub-pixel precision under varied Lunar constraints.

## Core Metrics (Registration_Metrics.py)
1. **RMSE (Root Mean Square Error)**: Measures the average point-to-point physical distance between reference keypoints and the re-projected source keypoints via the estimated Homography. Quantifies the structural distortion.
2. **TRE (Target Registration Error)**: Projects the four physical corners of the image boundary using both the Ground Truth Homography and the Predicted Homography, calculating the mean disparity. This is the ultimate, objective measure of full-image structural alignment accuracy.

## Automated Experimentation
- **BenchmarkSuite**: Can be dynamically wrapped around *any* functional component of the pipeline. It recursively scrapes the `data/synthetic` directory, calculates predicted structural matrices, and executes comparative L2 Norm error mapping against `ground_truth.json` files.
- **ComparativeAnalyzer**: Tracks runtime heuristics across multiple executions (e.g. comparing Baseline SIFT performance against Phase Congruency Pre-Processed SIFT).
- **AutoReportGenerator**: Condenses output scalars into dynamically generated Markdown briefs located in `docs/reports`.
- **EvaluationVisualizer**: Utilizes `matplotlib` to render absolute performance differentials, mapping improvement curves visually.
