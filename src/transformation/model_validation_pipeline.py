import numpy as np
import cv2
from typing import Tuple, Dict, Any

from src.transformation.model_fitter import ModelFitter
from src.transformation.model_selector import ModelSelector

class ModelValidationPipeline:
    """
    End-to-End Transformation Validation engine. Takes raw keypoints,
    fits multiple geometric topologies, and scores them to find the
    mathematically optimal alignment structure.
    """
    def __init__(self, config: Dict[str, Any] = None):
        ransac_thresh = config.get('ransac_thresh', 3.0) if config else 3.0
        self.fitter = ModelFitter(ransac_thresh)
        self.selector = ModelSelector()

    def select_transformation(self, kp1: list, kp2: list, matches: list, override_model: str = None) -> Tuple[str, np.ndarray, np.ndarray]:
        """
        Executes fitting and selection. Returns the optimal model name, matrix, and inlier mask.
        """
        if len(matches) < 4:
            raise ValueError("Not enough matches to compute geometric transformation (minimum 4).")
            
        # Extract coordinates
        pts1 = np.array([kp1[m.queryIdx].pt for m in matches], dtype=np.float32)
        pts2 = np.array([kp2[m.trainIdx].pt for m in matches], dtype=np.float32)
        
        # Fit all available models
        fitting_results = self.fitter.fit_all(pts1, pts2)
        
        if override_model and override_model in fitting_results:
            best_name = override_model
            best_data = fitting_results[override_model]
            best_data['rmse'] = self.selector._compute_reprojection_error(pts1, pts2, best_data['matrix'], best_data['mask'])
        else:
            # Score and select the best model automatically
            best_name, best_data = self.selector.select_best_model(pts1, pts2, fitting_results)
            
        if not best_name or best_data is None:
            raise ValueError("All models failed to fit. Geometric correspondence is invalid.")
            
        return best_name, best_data['matrix'], best_data['mask'], best_data.get('rmse', 0.0)
