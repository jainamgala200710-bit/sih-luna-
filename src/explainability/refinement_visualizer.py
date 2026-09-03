import numpy as np
import cv2
import os
from typing import Dict, Any

class RefinementVisualizer:
    """
    Visualizes and explains the mathematical effect of Phase Correlation 
    Sub-Pixel Refinement on a given coordinate point.
    """
    @staticmethod
    def explain_refinement(orig_kp: cv2.KeyPoint, refined_kp: cv2.KeyPoint) -> Dict[str, Any]:
        """
        Calculates the fractional vector translation between the integer keypoint 
        and the sub-pixel refined keypoint.
        """
        orig_pt = np.array(orig_kp.pt)
        ref_pt = np.array(refined_kp.pt)
        
        shift_vector = ref_pt - orig_pt
        shift_magnitude = np.linalg.norm(shift_vector)
        
        return {
            "Original Integer Coordinate": (round(orig_pt[0], 2), round(orig_pt[1], 2)),
            "Refined Sub-Pixel Coordinate": (round(ref_pt[0], 4), round(ref_pt[1], 4)),
            "Translation Vector (dx, dy)": (round(float(shift_vector[0]), 4), round(float(shift_vector[1]), 4)),
            "Translation Magnitude (px)": round(float(shift_magnitude), 4)
        }
