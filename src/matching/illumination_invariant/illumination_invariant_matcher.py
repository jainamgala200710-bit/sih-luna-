from typing import Tuple, List, Dict
import numpy as np
import cv2

from src.structural_features.phase_congruency import PhaseCongruencyEngine
from src.structural_features.gradient_orientation import GradientOrientationExtractor
from src.structural_features.structural_edge_maps import StructuralEdgeExtractor
from src.matching.classical.feature_matching_pipeline import ClassicalMatchingPipeline

class IlluminationInvariantMatcher:
    """
    Transforms input images into an illumination-invariant structural representation
    prior to executing feature matching.
    """
    def __init__(self, mode: str = 'phase_congruency', matcher_algo: str = 'SIFT'):
        self.mode = mode.lower()
        self.matcher = ClassicalMatchingPipeline(matcher_algo)
        
        if self.mode == 'phase_congruency':
            self.transformer = PhaseCongruencyEngine()
        elif self.mode == 'gradient':
            self.transformer = GradientOrientationExtractor()
        elif self.mode == 'edge':
            self.transformer = StructuralEdgeExtractor('canny')
        else:
            raise ValueError(f"Unknown structural transformation mode: {mode}")

    def run_matching(self, img1: np.ndarray, img2: np.ndarray) -> Tuple[list, list, list]:
        """
        Transforms images to structural maps, then runs matching.
        """
        # Transform inputs
        struct_img1 = self.transformer.compute(img1)
        struct_img2 = self.transformer.compute(img2)
        
        # Depending on the matcher, we may need to convert back to 3-channel
        # if the matcher internally converts to gray or expects standard format
        if len(struct_img1.shape) == 2:
            struct_img1 = cv2.cvtColor(struct_img1, cv2.COLOR_GRAY2BGR)
            struct_img2 = cv2.cvtColor(struct_img2, cv2.COLOR_GRAY2BGR)
            
        kp1, kp2, matches = self.matcher.run_matching(struct_img1, struct_img2)
        return kp1, kp2, matches
