import pytest
import cv2
import numpy as np
from src.matching.classical.feature_matching_pipeline import ClassicalMatchingPipeline
from src.utils.failure_warning_system import assert_minimum_matches, PipelineExhaustionError

def test_high_noise_exhaustion():
    """
    Tests that SIFT gracefully degrades when high-frequency Gaussian noise completely
    masks structural gradients.
    """
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(img1, (20, 20), (80, 80), (255, 255, 255), -1)
    
    # Introduce severe noise that completely replaces the image
    img2 = np.random.normal(128, 200, img1.shape).astype(np.float32)
    img2 = np.clip(img2, 0, 255).astype(np.uint8)
    img2 = np.clip(img2, 0, 255).astype(np.uint8)
    
    pipe = ClassicalMatchingPipeline('SIFT')
    kp1, kp2, matches = pipe.run_matching(img1, img2)
    
    with pytest.raises(PipelineExhaustionError):
        assert_minimum_matches(matches, minimum=4, stage="SIFT Matching")
