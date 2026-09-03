import cv2
import numpy as np
from typing import Tuple, Dict, Any

class ModelFitter:
    """
    Fits various geometric transformation models to a set of matched points.
    Supported models: 'homography', 'affine', 'partial_affine', 'translation'.
    """
    def __init__(self, ransac_thresh: float = 3.0):
        self.ransac_thresh = ransac_thresh

    def fit_homography(self, pts1: np.ndarray, pts2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Fits a full 3x3 projective transformation matrix."""
        H, mask = cv2.findHomography(pts1, pts2, cv2.USAC_MAGSAC, self.ransac_thresh)
        return H, mask

    def fit_affine(self, pts1: np.ndarray, pts2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Fits a 2x3 affine transformation matrix (rotation, scaling, translation, shear)."""
        A, mask = cv2.estimateAffine2D(pts1, pts2, method=cv2.RANSAC, ransacReprojThreshold=self.ransac_thresh)
        if A is not None:
            # Convert 2x3 to 3x3 for consistency
            H = np.vstack([A, [0, 0, 1]])
        else:
            H = None
        return H, mask

    def fit_partial_affine(self, pts1: np.ndarray, pts2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Fits a 2x3 partial affine transformation (rotation, uniform scaling, translation)."""
        A, mask = cv2.estimateAffinePartial2D(pts1, pts2, method=cv2.RANSAC, ransacReprojThreshold=self.ransac_thresh)
        if A is not None:
            H = np.vstack([A, [0, 0, 1]])
        else:
            H = None
        return H, mask

    def fit_all(self, pts1: np.ndarray, pts2: np.ndarray) -> Dict[str, Dict[str, Any]]:
        """Fits all available models and returns the matrices and masks."""
        results = {}
        
        H, h_mask = self.fit_homography(pts1, pts2)
        if H is not None:
            results['homography'] = {'matrix': H, 'mask': h_mask, 'inliers': np.sum(h_mask)}
            
        A, a_mask = self.fit_affine(pts1, pts2)
        if A is not None:
            results['affine'] = {'matrix': A, 'mask': a_mask, 'inliers': np.sum(a_mask)}
            
        PA, pa_mask = self.fit_partial_affine(pts1, pts2)
        if PA is not None:
            results['partial_affine'] = {'matrix': PA, 'mask': pa_mask, 'inliers': np.sum(pa_mask)}
            
        return results
