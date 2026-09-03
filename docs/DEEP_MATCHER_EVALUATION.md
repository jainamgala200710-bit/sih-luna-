# Deep Matcher Evaluation

## Overview
This document logs the evaluation of Deep Learning-based feature matchers designed to handle the complex illumination and texture challenges of Lunar imagery, extending beyond classical limits.

## Evaluated Frameworks
1. **LoFTR (Local Feature TRansformer)**: 
   - A detector-free matcher that utilizes self and cross attention layers in a Transformer architecture to obtain dense matches.
   - We utilize the pre-trained Kornia implementation (`kornia.feature.LoFTR`).
   - *Strengths*: Extremely robust to texture-less regions and massive illumination variations (common in lunar craters).
   - *Weaknesses*: Heavy computational cost. Requires a GPU and PyTorch/Kornia dependencies to run efficiently.

## Integration Architecture
- The pipeline wraps Kornia's tensors, executing inference, and maps the resulting grid coordinates and confidence scores back into OpenCV `cv2.KeyPoint` and `cv2.DMatch` objects. 
- This enables completely seamless integration with the existing `GeometricVerificationPipeline` (Phase 10) and `RegistrationPipeline` (Phase 11).

## Next Steps
Due to the environment requirements of PyTorch, running this pipeline locally requires the user to execute `pip install torch torchvision kornia`.
In Phase 13, we will benchmark this architecture against SIFT across varied datasets to quantify the improvement in true positive inlier ratios.
