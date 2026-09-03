import cv2
import numpy as np
from typing import Tuple, List

from src.multiscale.pyramid_builder import PyramidBuilder
from src.matching.classical.feature_matching_pipeline import ClassicalMatchingPipeline

class ScaleSpaceMatcher:
    """
    Implements Coarse-to-Fine Matching by executing feature extraction on
    scale-space pyramids and aggregating robust matches.
    """
    def __init__(self, matcher_algo: str = 'SIFT', levels: int = 3):
        self.matcher = ClassicalMatchingPipeline(matcher_algo)
        self.pyramid_engine = PyramidBuilder(levels)
        self.levels = levels

    def match_coarse_to_fine(self, img1: np.ndarray, img2: np.ndarray) -> Tuple[list, list, list]:
        """
        Executes multi-scale matching. Matches found at lower resolutions (coarse)
        are aggregated with matches at higher resolutions (fine).
        """
        pyr1 = self.pyramid_engine.build_gaussian_pyramid(img1)
        pyr2 = self.pyramid_engine.build_gaussian_pyramid(img2)
        
        all_kp1 = []
        all_kp2 = []
        all_matches = []
        
        match_idx_offset = 0
        
        # Iterate from the coarsest level (top of pyramid) to the finest (base)
        for i in reversed(range(len(pyr1))):
            level_img1 = pyr1[i]
            level_img2 = pyr2[i]
            
            # The scaling factor from this level back to the original resolution
            scale_factor = 2 ** i
            
            kp1, kp2, matches = self.matcher.run_matching(level_img1, level_img2)
            
            # Scale keypoint coordinates back to base resolution
            scaled_kp1 = []
            for kp in kp1:
                scaled_kp1.append(cv2.KeyPoint(x=kp.pt[0] * scale_factor, y=kp.pt[1] * scale_factor, size=kp.size * scale_factor))
                
            scaled_kp2 = []
            for kp in kp2:
                scaled_kp2.append(cv2.KeyPoint(x=kp.pt[0] * scale_factor, y=kp.pt[1] * scale_factor, size=kp.size * scale_factor))
                
            # Update match indices to avoid collisions when aggregated
            adjusted_matches = []
            for m in matches:
                adjusted_matches.append(cv2.DMatch(m.queryIdx + match_idx_offset, m.trainIdx + match_idx_offset, m.distance))
                
            all_kp1.extend(scaled_kp1)
            all_kp2.extend(scaled_kp2)
            all_matches.extend(adjusted_matches)
            
            # Increment offset by the number of keypoints added in this level
            match_idx_offset += max(len(kp1), len(kp2))
            
        return all_kp1, all_kp2, all_matches
