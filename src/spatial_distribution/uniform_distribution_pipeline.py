from typing import Tuple, Dict, Any
import numpy as np
import cv2

from src.spatial_distribution.grid_based_suppression import GridBasedSuppression
from src.spatial_distribution.distribution_metrics import DistributionMetrics

class UniformDistributionPipeline:
    """
    Acts as a post-processing layer following feature extraction and geometric verification.
    Enforces a strict uniform spatial distribution over the image to prevent model drift
    and overfitting to heavily clustered terrain features (e.g. tight crater clusters).
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.grid_size = config.get('grid_size', (4, 4)) if config else (4, 4)
        self.max_per_cell = config.get('max_per_cell', 10) if config else 10
        self.suppressor = GridBasedSuppression(self.grid_size, self.max_per_cell)
        
    def filter_matches(self, kp1: list, kp2: list, matches: list, image_shape: Tuple[int, int]) -> Tuple[list, dict]:
        """
        Executes suppression and returns filtered matches alongside metric improvements.
        """
        # Baseline metrics
        initial_metrics = DistributionMetrics.compute_metrics(kp1, matches, image_shape, self.grid_size)
        
        # Filter
        filtered_matches = self.suppressor.suppress(kp1, kp2, matches, image_shape)
        
        # Post-filter metrics
        final_metrics = DistributionMetrics.compute_metrics(kp1, filtered_matches, image_shape, self.grid_size)
        
        results = {
            "initial": initial_metrics,
            "final": final_metrics,
            "matches_suppressed": len(matches) - len(filtered_matches)
        }
        
        return filtered_matches, results
