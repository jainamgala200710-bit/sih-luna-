import pytest
import cv2
import numpy as np
from src.matching.classical.feature_matching_pipeline import ClassicalMatchingPipeline
from src.utils.failure_warning_system import assert_minimum_matches, PipelineExhaustionError

def test_scale_exhaustion():
    """
    Tests that SIFT gracefully degrades when facing a 20x scale differential (like OHRC vs TMC2)
    which physically breaks the Gaussian Difference octave parameters.
    """
    # Base high-res image
    img1 = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.rectangle(img1, (100, 100), (300, 300), (255, 255, 255), -1)
    cv2.circle(img1, (200, 200), 50, (128, 128, 128), -1)
    
    # Extreme downscale (20x)
    img2 = cv2.resize(img1, (20, 20))
    
    pipe = ClassicalMatchingPipeline('SIFT')
    kp1, kp2, matches = pipe.run_matching(img1, img2)
    
    with pytest.raises(PipelineExhaustionError):
        assert_minimum_matches(matches, minimum=4, stage="SIFT Matching")
