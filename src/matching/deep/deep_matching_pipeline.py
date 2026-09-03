from typing import Dict, Any, Tuple
import numpy as np
import os
import cv2

from src.matching.deep.loftr_matcher import LoFTRMatcher

class DeepMatchingPipeline:
    """
    Orchestrates deep learning-based feature matching.
    Currently integrates LoFTR.
    """
    def __init__(self, algorithm: str = 'LOFTR', config: Dict[str, Any] = None):
        self.algorithm = algorithm.upper()
        if self.algorithm == 'LOFTR':
            pretrained = config.get('pretrained', 'outdoor') if config else 'outdoor'
            conf = config.get('confidence_threshold', 0.2) if config else 0.2
            self.matcher = LoFTRMatcher(pretrained=pretrained, confidence_threshold=conf)
        else:
            raise ValueError(f"Unsupported deep algorithm: {algorithm}")
            
    def run_matching(self, img1: np.ndarray, img2: np.ndarray) -> Tuple[list, list, list]:
        """
        Runs the deep matching model and returns keypoints and matches.
        """
        kp1, kp2, matches = self.matcher.match(img1, img2)
        return kp1, kp2, matches
        
    def visualize_matches(self, img1: np.ndarray, kp1: list, img2: np.ndarray, kp2: list, matches: list, output_path: str = None) -> np.ndarray:
        """
        Draws matches between the two images.
        """
        # Sort by distance (1 - confidence)
        sorted_matches = sorted(matches, key=lambda x: x.distance)
        display_matches = sorted_matches[:100] # Limit for visibility
        
        match_img = cv2.drawMatches(
            img1, kp1, img2, kp2, display_matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            cv2.imwrite(output_path, match_img)
            
        return match_img
