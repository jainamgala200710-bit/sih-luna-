import pytest
import cv2
import numpy as np
import os
from src.matching.classical.feature_matching_pipeline import ClassicalMatchingPipeline
from src.utils.failure_warning_system import assert_minimum_matches, PipelineExhaustionError

def test_illumination_exhaustion():
    """
    Tests that SIFT gracefully throws PipelineExhaustionError when the illumination gradient
    is physically too severe to find nearest-neighbor gradients.
    """
    # Create synthetic test imagery directly in memory
    img1 = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    # Introduce some fake structure so it's not totally blank
    cv2.circle(img1, (50, 50), 20, (255, 255, 255), -1)
    cv2.circle(img1, (20, 20), 10, (0, 0, 0), -1)
    
    # Image 2 is heavily darkened (extreme illumination variance)
    img2 = (img1.astype(np.float32) * 0.1).astype(np.uint8)
    
    pipe = ClassicalMatchingPipeline('SIFT')
    kp1, kp2, matches = pipe.run_matching(img1, img2)
    
    # SIFT should fail to find 4 robust matches under such extreme global darkening
    # We assert that the graceful degradation wrapper catches this correctly
    with pytest.raises(PipelineExhaustionError) as excinfo:
        assert_minimum_matches(matches, minimum=4, stage="SIFT Matching")
        
    assert "Insufficient matching geometry" in str(excinfo.value)
