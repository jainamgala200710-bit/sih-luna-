import numpy as np
import cv2
from typing import Dict, Any

class GeometricConsistencyChecker:
    """
    Explains *why* a specific match was accepted or rejected by the Geometric Verifier
    by calculating its independent reprojection error against the global Homography.
    """
    @staticmethod
    def analyze_match(kp1: cv2.KeyPoint, kp2: cv2.KeyPoint, H: np.ndarray, thresh: float = 3.0) -> Dict[str, Any]:
        """
        Projects kp1 using H and calculates its geometric distance to kp2.
        """
        pt1 = np.array([kp1.pt], dtype=np.float32).reshape(-1, 1, 2)
        pt2 = np.array(kp2.pt, dtype=np.float32)
        
        # Reproject
        pt1_proj = cv2.perspectiveTransform(pt1, H).reshape(2,)
        
        # Calculate error
        error = np.linalg.norm(pt2 - pt1_proj)
        
        status = "Inlier (Accepted)" if error <= thresh else "Outlier (Rejected)"
        
        return {
            "Geometric Status": status,
            "Calculated Reprojection Error (px)": round(float(error), 3),
            "Allowed Threshold (px)": thresh,
            "Projected Coordinates (x,y)": (round(float(pt1_proj[0]), 3), round(float(pt1_proj[1]), 3)),
            "Actual Target Coordinates (x,y)": (round(float(pt2[0]), 3), round(float(pt2[1]), 3))
        }
