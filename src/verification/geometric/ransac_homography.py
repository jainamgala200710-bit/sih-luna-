import cv2
import numpy as np
from typing import Tuple, List, Dict

class RANSACHomographyVerifier:
    """
    Implements standard RANSAC geometric verification to filter false feature matches.
    """
    def __init__(self, reproj_threshold: float = 3.0, max_iters: int = 2000, confidence: float = 0.995):
        self.reproj_threshold = reproj_threshold
        self.max_iters = max_iters
        self.confidence = confidence

    def verify(self, kp1: list, kp2: list, matches: list) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates homography using RANSAC and returns the matrix and an inlier mask.
        """
        if len(matches) < 4:
            return None, None
            
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        
        H, mask = cv2.findHomography(
            src_pts, 
            dst_pts, 
            cv2.RANSAC, 
            self.reproj_threshold,
            None,
            self.max_iters,
            self.confidence
        )
        
        return H, mask

    def extract_inliers(self, matches: list, mask: np.ndarray) -> List[cv2.DMatch]:
        """Filters match list down to only inliers based on the mask."""
        if mask is None:
            return []
        return [m for i, m in enumerate(matches) if mask[i][0] == 1]
