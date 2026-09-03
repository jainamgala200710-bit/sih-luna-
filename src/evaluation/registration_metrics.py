import numpy as np
import cv2
from typing import Tuple, Dict

class RegistrationMetrics:
    """
    Computes rigorous spatial and geometric metrics to evaluate the alignment
    accuracy of the final transformed image against the reference frame.
    """
    @staticmethod
    def compute_rmse(pts_source: np.ndarray, pts_ref: np.ndarray, H: np.ndarray) -> float:
        """Computes Root Mean Square Error (RMSE) of reprojected points."""
        if len(pts_source) == 0:
            return float('inf')
            
        pts_src_reshape = pts_source.reshape(-1, 1, 2)
        pts_src_transformed = cv2.perspectiveTransform(pts_src_reshape, H).reshape(-1, 2)
        
        errors = np.linalg.norm(pts_ref - pts_src_transformed, axis=1)
        return float(np.sqrt(np.mean(errors ** 2)))
        
    @staticmethod
    def compute_tre(gt_H: np.ndarray, pred_H: np.ndarray, image_shape: Tuple[int, int]) -> float:
        """
        Computes Target Registration Error (TRE).
        We calculate this by warping the 4 corners of the image using the Ground Truth H
        and comparing those coordinates to corners warped by the Predicted H.
        """
        h, w = image_shape[:2]
        corners = np.array([
            [0, 0],
            [w, 0],
            [w, h],
            [0, h]
        ], dtype=np.float32).reshape(-1, 1, 2)
        
        gt_corners = cv2.perspectiveTransform(corners, gt_H).reshape(-1, 2)
        pred_corners = cv2.perspectiveTransform(corners, pred_H).reshape(-1, 2)
        
        errors = np.linalg.norm(gt_corners - pred_corners, axis=1)
        return float(np.mean(errors))

    @staticmethod
    def full_evaluation(pts_src: np.ndarray, pts_ref: np.ndarray, pred_H: np.ndarray, gt_H: np.ndarray, image_shape: Tuple[int, int]) -> Dict[str, float]:
        """Calculates and aggregates all geometric metrics."""
        return {
            "rmse": RegistrationMetrics.compute_rmse(pts_src, pts_ref, pred_H),
            "tre": RegistrationMetrics.compute_tre(gt_H, pred_H, image_shape)
        }
