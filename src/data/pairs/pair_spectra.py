import cv2
import numpy as np
import os

class PairVisualizer:
    """
    Visualizes image pairs and their relationships.
    """
    def __init__(self):
        pass
        
    def visualize_pair(self, source_img: np.ndarray, ref_img: np.ndarray, output_path: str = None) -> np.ndarray:
        """
        Creates a side-by-side visualization of the source and reference images.
        """
        # Ensure both are same type and channels
        if len(source_img.shape) == 2:
            s_vis = cv2.cvtColor(source_img, cv2.COLOR_GRAY2BGR)
        else:
            s_vis = source_img.copy()
            
        if len(ref_img.shape) == 2:
            r_vis = cv2.cvtColor(ref_img, cv2.COLOR_GRAY2BGR)
        else:
            r_vis = ref_img.copy()
            
        # Resize to same height for side-by-side display
        target_h = max(s_vis.shape[0], r_vis.shape[0])
        
        s_vis_r = cv2.resize(s_vis, (int(s_vis.shape[1] * target_h / s_vis.shape[0]), target_h))
        r_vis_r = cv2.resize(r_vis, (int(r_vis.shape[1] * target_h / r_vis.shape[0]), target_h))
        
        # Add labels
        cv2.putText(s_vis_r, "Source", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(r_vis_r, "Reference", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        combined = np.hstack((s_vis_r, r_vis_r))
        
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            cv2.imwrite(output_path, combined)
            
        return combined
