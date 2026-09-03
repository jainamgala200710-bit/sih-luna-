import cv2
import numpy as np
from typing import Tuple, List

class SIFTMatcher:
    """
    Implements SIFT (Scale-Invariant Feature Transform) feature detection,
    description, and matching using FLANN.
    """
    def __init__(self, nfeatures: int = 0, nOctaveLayers: int = 3, contrastThreshold: float = 0.04, edgeThreshold: float = 10, sigma: float = 1.6):
        # Initialize SIFT detector
        self.sift = cv2.SIFT_create(
            nfeatures=nfeatures,
            nOctaveLayers=nOctaveLayers,
            contrastThreshold=contrastThreshold,
            edgeThreshold=edgeThreshold,
            sigma=sigma
        )
        
        # FLANN parameters for SIFT (KDTree)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50) # or pass empty dictionary
        self.matcher = cv2.FlannBasedMatcher(index_params, search_params)

    def detect_and_compute(self, image: np.ndarray) -> Tuple[List[cv2.KeyPoint], np.ndarray]:
        """Detects keypoints and computes descriptors."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        keypoints, descriptors = self.sift.detectAndCompute(gray, None)
        return keypoints, descriptors

    def match(self, des1: np.ndarray, des2: np.ndarray, ratio_threshold: float = 0.75) -> List[cv2.DMatch]:
        """
        Matches descriptors using FLANN and applies Lowe's ratio test.
        """
        if des1 is None or len(des1) < 2 or des2 is None or len(des2) < 2:
            return []
            
        matches = self.matcher.knnMatch(des1, des2, k=2)
        
        # Apply Lowe's ratio test
        good_matches = []
        for m_n in matches:
            if len(m_n) != 2:
                continue
            m, n = m_n
            if m.distance < ratio_threshold * n.distance:
                good_matches.append(m)
                
        return good_matches
