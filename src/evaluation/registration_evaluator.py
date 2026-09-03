import numpy as np
import json
from typing import Dict, Any
import cv2

class RegistrationEvaluator:
    """
    Evaluates the final computed homography against the ground truth.
    Calculates Corner Error (Mean Target Registration Error on image corners).
    """
    def __init__(self, ground_truth_path: str):
        with open(ground_truth_path, 'r') as f:
            self.gt = json.load(f)
        self.H_gt = np.array(self.gt['homography'])

    def evaluate_homography(self, H_est: np.ndarray, image_shape: tuple) -> Dict[str, Any]:
        """
        Calculates the mean pixel distance error on the four corners of the image
        when projected by H_est versus H_gt.
        """
        if H_est is None:
            return {"error_mean": float('inf'), "status": "failed"}
            
        h, w = image_shape[:2]
        corners = np.array([
            [0, 0, 1],
            [w, 0, 1],
            [w, h, 1],
            [0, h, 1]
        ], dtype=np.float64).T
        
        # Project using ground truth
        gt_proj = np.dot(self.H_gt, corners)
        gt_proj = gt_proj[:2, :] / gt_proj[2, :]
        
        # Project using estimated H
        est_proj = np.dot(H_est, corners)
        est_proj = est_proj[:2, :] / est_proj[2, :]
        
        # Calculate Euclidean distances for each corner
        distances = np.linalg.norm(gt_proj - est_proj, axis=0)
        
        return {
            "error_mean": float(np.mean(distances)),
            "error_max": float(np.max(distances)),
            "status": "evaluated"
        }
