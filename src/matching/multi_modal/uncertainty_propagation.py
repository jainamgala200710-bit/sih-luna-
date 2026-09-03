import numpy as np
from typing import List, Dict

class UncertaintyPropagator:
    """
    Estimates the spatial uncertainty of keypoints based on the scale pyramid level
    they were extracted from.
    """
    def __init__(self, base_uncertainty_pixels: float = 0.5):
        self.base_uncertainty = base_uncertainty_pixels

    def compute_uncertainty(self, level: int) -> float:
        """
        Computes spatial uncertainty. 
        A match found at level 1 (1/2 resolution) has 2x the uncertainty of a match at level 0.
        """
        scale_factor = 2 ** level
        return self.base_uncertainty * scale_factor
        
    def weight_matches(self, matches: list, level: int) -> list:
        """
        Optionally adjust the distance/confidence of matches based on their scale uncertainty.
        Matches with higher uncertainty have their distances artificially inflated to
        deprioritize them when mixed with native-resolution matches.
        """
        uncertainty = self.compute_uncertainty(level)
        
        # We increase the distance metric of the match by a factor of the uncertainty
        # so that fine-grained matches are preferred when sorting by distance.
        weighted_matches = []
        for m in matches:
            import cv2
            weighted_matches.append(cv2.DMatch(m.queryIdx, m.trainIdx, m.distance * uncertainty))
            
        return weighted_matches
