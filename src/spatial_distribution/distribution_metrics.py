import numpy as np
from typing import Tuple, Dict

class DistributionMetrics:
    """
    Computes spatial coverage and uniformity metrics to quantify 
    how well matches are distributed across an image.
    """
    @staticmethod
    def compute_metrics(kp: list, matches: list, image_shape: Tuple[int, int], grid_size: Tuple[int, int] = (4, 4)) -> Dict[str, float]:
        if not matches:
            return {"coverage_percent": 0.0, "entropy": 0.0}
            
        h, w = image_shape[:2]
        grid_rows, grid_cols = grid_size
        
        cell_h = h / grid_rows
        cell_w = w / grid_cols
        
        grid_counts = np.zeros((grid_rows, grid_cols), dtype=int)
        
        for m in matches:
            pt = kp[m.queryIdx].pt
            row_idx = min(max(int(pt[1] // cell_h), 0), grid_rows - 1)
            col_idx = min(max(int(pt[0] // cell_w), 0), grid_cols - 1)
            grid_counts[row_idx, col_idx] += 1
            
        total_cells = grid_rows * grid_cols
        filled_cells = np.count_nonzero(grid_counts)
        coverage = (filled_cells / total_cells) * 100.0
        
        # Calculate spatial entropy (measure of evenness)
        total_matches = len(matches)
        if total_matches == 0:
            entropy = 0.0
        else:
            probs = grid_counts[grid_counts > 0] / total_matches
            entropy = -np.sum(probs * np.log2(probs))
            
        return {
            "coverage_percent": coverage,
            "entropy": entropy,
            "total_matches": total_matches
        }
