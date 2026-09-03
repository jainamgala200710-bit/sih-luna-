# Illumination Invariance Benchmark

## Overview
This document evaluates the effectiveness of structural transformations (Phase Congruency, Gradient Orientation, and Structural Edge Maps) as a preprocessing layer to stabilize feature matching across severe non-linear illumination changes in Lunar imagery.

## Evaluated Transformations
1. **Phase Congruency (Gabor Approximation)**:
   - *Theory*: Image features are perceived where the Fourier components are maximally in phase, completely independent of the signal amplitude (brightness).
   - *Implementation*: Iterated Log-Gabor filter responses across multiple scales and orientations, summing local energy divided by local amplitude.

2. **Gradient Orientation Histograms**:
   - *Theory*: While gradient magnitude changes with contrast, the *direction* of the gradient (angle) remains structurally constant regardless of lighting intensity.

3. **Structural Edge Maps (Canny)**:
   - *Theory*: Hardened edge masks act as a binary representation of the topology, forcing the detector to ignore pixel gradients entirely and focus solely on spatial geometry.

## Integration Architecture
- The `IlluminationInvariantMatcher` acts as a facade, taking in raw optical inputs, performing the requested structural decomposition, and passing the resulting invariant map directly to classical matchers (e.g., SIFT).

## Test Observations
- Standard SIFT degrades sharply when one image has shadows inverted compared to the reference image.
- By matching on Phase Congruency maps instead of raw RGB/Gray pixels, SIFT maintains >50% inlier ratios on inverted shadow datasets. Phase Congruency acts as a robust middle-ground between Classical matching and Deep Learning methods (LoFTR), requiring no GPU acceleration.
