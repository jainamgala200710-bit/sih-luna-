import cv2
import numpy as np
import os

class FeatureSimilarityVisualizer:
    """
    Renders visual debug images comparing the local neighborhood patches
    surrounding a paired feature match. This allows human verification
    that the extracted structures actually resemble each other.
    """
    def __init__(self, output_dir: str = "docs/reports/explainability"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def visualize_patch(self, src_img: np.ndarray, ref_img: np.ndarray, 
                        kp1: cv2.KeyPoint, kp2: cv2.KeyPoint, match_id: str, 
                        window_size: int = 40) -> str:
        """
        Extracts `window_size` patches around kp1 and kp2, resizes them,
        and tiles them horizontally for visual comparison.
        """
        half_win = window_size // 2
        
        # Ensure images are Grayscale for patch comparison
        if len(src_img.shape) == 3:
            s_gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        else:
            s_gray = src_img
            
        if len(ref_img.shape) == 3:
            r_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
        else:
            r_gray = ref_img
            
        h1, w1 = s_gray.shape
        h2, w2 = r_gray.shape
        
        x1, y1 = int(kp1.pt[0]), int(kp1.pt[1])
        x2, y2 = int(kp2.pt[0]), int(kp2.pt[1])
        
        # Boundary clipping
        y1_start, y1_end = max(0, y1-half_win), min(h1, y1+half_win)
        x1_start, x1_end = max(0, x1-half_win), min(w1, x1+half_win)
        
        y2_start, y2_end = max(0, y2-half_win), min(h2, y2+half_win)
        x2_start, x2_end = max(0, x2-half_win), min(w2, x2+half_win)
        
        patch1 = s_gray[y1_start:y1_end, x1_start:x1_end]
        patch2 = r_gray[y2_start:y2_end, x2_start:x2_end]
        
        # Resize patches for easier viewing (scale up by 4x)
        if patch1.size > 0 and patch2.size > 0:
            patch1_display = cv2.resize(patch1, (window_size * 4, window_size * 4), interpolation=cv2.INTER_NEAREST)
            patch2_display = cv2.resize(patch2, (window_size * 4, window_size * 4), interpolation=cv2.INTER_NEAREST)
            
            # Tile horizontally
            combined = np.hstack((patch1_display, patch2_display))
            
            # Save image
            filename = f"match_patch_{match_id}.png"
            filepath = os.path.join(self.output_dir, filename)
            cv2.imwrite(filepath, combined)
            return filepath
            
        return ""
