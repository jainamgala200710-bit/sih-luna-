import numpy as np
import cv2
from typing import Dict, Any, Tuple

class ModelSelector:
    """
    Evaluates geometric models and dynamically selects the optimal transformation.
    """
    def __init__(self):
        # Degrees of Freedom for each model type to penalize overly complex models (AIC/BIC inspired)
        self.dof = {
            'homography': 8,
            'affine': 6,
            'partial_affine': 4
        }
        
    def _compute_reprojection_error(self, pts1: np.ndarray, pts2: np.ndarray, H: np.ndarray, mask: np.ndarray) -> float:
        """Computes Root Mean Square Error (RMSE) for the inlier points."""
        inliers_idx = np.where(mask.ravel() == 1)[0]
        if len(inliers_idx) == 0:
            return float('inf')
            
        pts1_in = pts1[inliers_idx]
        pts2_in = pts2[inliers_idx]
        
        # Transform pts1 using H
        pts1_in_reshape = pts1_in.reshape(-1, 1, 2)
        pts1_transformed = cv2.perspectiveTransform(pts1_in_reshape, H).reshape(-1, 2)
        
        # Compute L2 norm (Euclidean distance)
        errors = np.linalg.norm(pts2_in - pts1_transformed, axis=1)
        rmse = np.sqrt(np.mean(errors ** 2))
        return rmse

    def select_best_model(self, pts1: np.ndarray, pts2: np.ndarray, fitting_results: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """
        Selects the optimal model balancing Inlier Count, Reprojection Error, and Model Complexity.
        """
        best_model_name = None
        best_score = float('inf')
        
        for name, data in fitting_results.items():
            H = data['matrix']
            mask = data['mask']
            inliers = data['inliers']
            
            # Minimum points required to trust a model
            if inliers < self.dof[name]:
                continue
                
            rmse = self._compute_reprojection_error(pts1, pts2, H, mask)
            
            # Compute a heuristic score: RMSE * (Penalty for complexity) / log(Inliers)
            # Lower score is better
            complexity_penalty = 1.0 + (self.dof[name] * 0.05)
            score = (rmse * complexity_penalty) / np.log(inliers + 1)
            
            data['rmse'] = rmse
            data['score'] = score
            
            if score < best_score:
                best_score = score
                best_model_name = name
                
        return best_model_name, fitting_results[best_model_name] if best_model_name else None
