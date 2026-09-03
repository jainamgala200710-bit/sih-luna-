import cv2
import os
import numpy as np
from src.visualization.plot_utils import create_blended_overlay, create_checkerboard, create_difference_image

class PairVisualizerSuite:
    """
    Advanced visualizer suite for generating complete visualization grids
    for image pairs.
    """
    def __init__(self, output_dir: str = "results/visualizations"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_comparison_grid(self, source_img: np.ndarray, ref_img: np.ndarray, pair_id: str):
        """
        Generates a 2x2 comparison grid:
        [Source]        [Reference]
        [Checkerboard]  [Difference]
        """
        # Ensure sizes match by padding/resizing if necessary
        # For our synthetic dataset, sizes usually match unless scaled, but homography warp 
        # keeps canvas size the same.
        if source_img.shape != ref_img.shape:
            ref_img = cv2.resize(ref_img, (source_img.shape[1], source_img.shape[0]))
            
        # Convert grayscale to BGR for consistent visual output
        if len(source_img.shape) == 2:
            source_img = cv2.cvtColor(source_img, cv2.COLOR_GRAY2BGR)
        if len(ref_img.shape) == 2:
            ref_img = cv2.cvtColor(ref_img, cv2.COLOR_GRAY2BGR)
            
        checker = create_checkerboard(source_img, ref_img)
        diff = create_difference_image(source_img, ref_img)
        
        # Add labels
        cv2.putText(source_img, "Source", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(ref_img, "Reference", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(checker, "Checkerboard", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(diff, "Difference", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Create grid
        top = np.hstack((source_img, ref_img))
        bottom = np.hstack((checker, diff))
        grid = np.vstack((top, bottom))
        
        out_path = os.path.join(self.output_dir, f"{pair_id}_comparison.png")
        cv2.imwrite(out_path, grid)
        return out_path
