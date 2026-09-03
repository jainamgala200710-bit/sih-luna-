# Synthetic Lunar Dataset

This directory (`data/synthetic/`) contains synthetically generated lunar image pairs designed for testing the LunaAlign AI registration and correspondence algorithms.

## Dataset Structure
Each pair is stored in its own numbered directory (e.g., `pair_001/`):
- `source.png`: The transformed image (simulating e.g. Chandrayaan-2)
- `reference.png`: The base image (simulating e.g. LRO NAC)
- `metadata.json`: Contains the parameters used to generate the source image (transformation, illumination changes, noise).
- `ground_truth.json`: Contains the ground truth homography/affine matrix mapping pixels from the source image to the reference image.

## Generation Process
The generation pipeline performs the following steps:
1. **Base Image Generation**: A procedural lunar surface (or a real high-resolution tile) is used as the reference image.
2. **Geometric Transformation**: The base image is subjected to random translation, rotation, scaling, and perspective distortion to simulate viewpoint changes.
3. **Illumination Variation**: Contrast adjustments, gamma corrections, and simulated shadow direction changes are applied to simulate different solar azimuths and elevations.
4. **Degradation**: Gaussian noise and blur are added to simulate sensor noise and differing resolutions.

## Usage
These synthetic pairs provide a perfect ground truth for verifying:
- Feature detector robustness to illumination changes.
- Sub-pixel refinement accuracy.
- Geometric verification (RANSAC/USAC) stability.

See `src/data/generation/synthetic_data_generator.py` for the code that generates this dataset.
