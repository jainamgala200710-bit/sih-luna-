import numpy as np
import cv2
import os

class UncertaintyVisualizer:
    """
    Renders visual heatmaps overlaying the predicted covariance/uncertainty 
    matrix around a localized extracted keypoint.
    """
    def __init__(self, output_dir: str = "docs/reports/explainability"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def visualize_uncertainty(self, img: np.ndarray, kp: cv2.KeyPoint, match_id: str, radius_multiplier: float = 1.0) -> str:
        """
        Draws a circle indicating the spatial blur scale where the keypoint was found.
        Features extracted at higher pyramid octaves possess mathematically wider bounds of spatial uncertainty.
        """
        if len(img.shape) == 2:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            vis = img.copy()
            
        x, y = int(kp.pt[0]), int(kp.pt[1])
        
        # In scale-space theory, spatial uncertainty is proportional to the Gaussian blur sigma 
        # (which maps to the feature's size property).
        uncertainty_radius = int((kp.size / 2) * radius_multiplier)
        
        # Draw central point
        cv2.circle(vis, (x, y), 2, (0, 0, 255), -1)
        
        # Draw uncertainty boundary (representing 1-sigma distribution)
        cv2.circle(vis, (x, y), max(1, uncertainty_radius), (0, 255, 255), 2)
        
        filename = f"uncertainty_kp_{match_id}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crop for viewing context
        h, w = vis.shape[:2]
        crop_size = max(50, uncertainty_radius * 4)
        
        y_start, y_end = max(0, y-crop_size), min(h, y+crop_size)
        x_start, x_end = max(0, x-crop_size), min(w, x+crop_size)
        
        crop = vis[y_start:y_end, x_start:x_end]
        
        if crop.size > 0:
            cv2.imwrite(filepath, crop)
            return filepath
        return ""
