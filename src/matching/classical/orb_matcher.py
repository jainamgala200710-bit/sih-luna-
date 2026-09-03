import cv2
import numpy as np
from typing import Tuple, List

class ORBMatcher:
    """
    Implements ORB (Oriented FAST and Rotated BRIEF) feature detection,
    description, and matching using Brute Force Matcher with Hamming distance.
    """
    def __init__(self, nfeatures: int = 5000, scaleFactor: float = 1.2, nlevels: int = 8, edgeThreshold: int = 31):
        # Initialize ORB detector
        self.orb = cv2.ORB_create(
            nfeatures=nfeatures,
            scaleFactor=scaleFactor,
            nlevels=nlevels,
            edgeThreshold=edgeThreshold
        )
        
        # FLANN parameters for ORB (LSH)
        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH,
                            table_number=6, # 12
                            key_size=12,     # 20
                            multi_probe_level=1) #2
        search_params = dict(checks=50)
        self.matcher = cv2.FlannBasedMatcher(index_params, search_params)

    def detect_and_compute(self, image: np.ndarray) -> Tuple[List[cv2.KeyPoint], np.ndarray]:
        """Detects keypoints and computes descriptors."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        return keypoints, descriptors

    def match(self, des1: np.ndarray, des2: np.ndarray, ratio_threshold: float = 0.8) -> List[cv2.DMatch]:
        """
        Matches descriptors using BFMatcher and applies Lowe's ratio test.
        """
        if des1 is None or len(des1) < 2 or des2 is None or len(des2) < 2:
            return []
            
        matches = self.matcher.knnMatch(des1, des2, k=2)
        
        good_matches = []
        for m_n in matches:
            if len(m_n) != 2:
                continue
            m, n = m_n
            # Ensure distance scale for Hamming is meaningful for ratio test.
            # While ratio test is less theoretical for binary descriptors, it works empirically.
            if m.distance < ratio_threshold * n.distance:
                good_matches.append(m)
                
        return good_matches
