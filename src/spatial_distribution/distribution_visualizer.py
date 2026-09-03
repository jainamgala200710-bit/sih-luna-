import cv2
import numpy as np
import os
from typing import Tuple

class DistributionVisualizer:
    """
    Visualizes the spatial grid and match distribution.
    """
    def __init__(self, output_dir: str = "results/distribution"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def visualize(self, image: np.ndarray, kp: list, matches: list, grid_size: Tuple[int, int], output_name: str) -> str:
        """
        Draws the grid over the image and plots the retained keypoints.
        """
        if len(image.shape) == 2:
            vis = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            vis = image.copy()
            
        h, w = vis.shape[:2]
        grid_rows, grid_cols = grid_size
        
        cell_h = int(h / grid_rows)
        cell_w = int(w / grid_cols)
        
        # Draw grid lines
        for i in range(1, grid_cols):
            cv2.line(vis, (i * cell_w, 0), (i * cell_w, h), (200, 200, 200), 1)
        for i in range(1, grid_rows):
            cv2.line(vis, (0, i * cell_h), (w, i * cell_h), (200, 200, 200), 1)
            
        # Draw keypoints
        for m in matches:
            pt = kp[m.queryIdx].pt
            cv2.circle(vis, (int(pt[0]), int(pt[1])), 4, (0, 255, 0), -1)
            
        out_path = os.path.join(self.output_dir, output_name)
        cv2.imwrite(out_path, vis)
        
        return out_path
