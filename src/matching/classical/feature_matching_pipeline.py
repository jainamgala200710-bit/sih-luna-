import cv2
import numpy as np
from typing import Dict, Any, Tuple
import os

from src.matching.classical.sift_matcher import SIFTMatcher
from src.matching.classical.orb_matcher import ORBMatcher

class ClassicalMatchingPipeline:
    """
    Orchestrates classical feature matching between image pairs.
    """
    def __init__(self, algorithm: str = 'SIFT', config: Dict[str, Any] = None):
        self.algorithm = algorithm.upper()
        if self.algorithm == 'SIFT':
            self.matcher = SIFTMatcher()
            self.ratio = config.get('ratio_threshold', 0.75) if config else 0.75
        elif self.algorithm == 'ORB':
            self.matcher = ORBMatcher()
            self.ratio = config.get('ratio_threshold', 0.8) if config else 0.8
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
            
    def run_matching(self, img1: np.ndarray, img2: np.ndarray) -> Tuple[list, list, list]:
        """
        Runs the full matching pipeline and returns keypoints and good matches.
        """
        kp1, des1 = self.matcher.detect_and_compute(img1)
        kp2, des2 = self.matcher.detect_and_compute(img2)
        
        good_matches = self.matcher.match(des1, des2, ratio_threshold=self.ratio)
        return kp1, kp2, good_matches
        
    def visualize_matches(self, img1: np.ndarray, kp1: list, img2: np.ndarray, kp2: list, matches: list, output_path: str = None) -> np.ndarray:
        """
        Draws matches between the two images.
        """
        # Draw top matches (sort by distance)
        sorted_matches = sorted(matches, key=lambda x: x.distance)
        # Limit to top 100 for visual clarity
        display_matches = sorted_matches[:100]
        
        match_img = cv2.drawMatches(
            img1, kp1, img2, kp2, display_matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            cv2.imwrite(output_path, match_img)
            
        return match_img
