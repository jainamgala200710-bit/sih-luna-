import cv2
import numpy as np
from typing import Tuple, List

class USACVerifier:
    """
    Implements USAC/MAGSAC++ geometric verification for advanced outlier rejection.
    MAGSAC++ does not strictly require an inlier threshold parameter as it marginalizes over it.
    """
    def __init__(self, reproj_threshold: float = 3.0, max_iters: int = 10000, confidence: float = 0.999):
        self.reproj_threshold = reproj_threshold
        self.max_iters = max_iters
        self.confidence = confidence

    def verify(self, kp1: list, kp2: list, matches: list) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates homography using MAGSAC++ and returns the matrix and an inlier mask.
        Falls back to RANSAC if USAC is unavailable in the current OpenCV version.
        """
        if len(matches) < 4:
            return None, None
            
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        
        # Check if MAGSAC++ is available
        if hasattr(cv2, 'USAC_MAGSAC'):
            method = cv2.USAC_MAGSAC
        else:
            method = cv2.RANSAC
            
        H, mask = cv2.findHomography(
            src_pts, 
            dst_pts, 
            method, 
            self.reproj_threshold,
            None,
            self.max_iters,
            self.confidence
        )
        
        return H, mask

    def extract_inliers(self, matches: list, mask: np.ndarray) -> List[cv2.DMatch]:
        if mask is None:
            return []
        return [m for i, m in enumerate(matches) if mask[i][0] == 1]
