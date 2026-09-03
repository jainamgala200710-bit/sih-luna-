import numpy as np
import cv2
from typing import List, Tuple

class GridBasedSuppression:
    """
    Suppresses clustered feature matches to enforce a uniform spatial distribution.
    Divides the image into a grid and enforces a maximum number of matches per grid cell,
    prioritizing matches with higher confidence (lower distance).
    """
    def __init__(self, grid_size: Tuple[int, int] = (4, 4), max_per_cell: int = 10):
        self.grid_rows, self.grid_cols = grid_size
        self.max_per_cell = max_per_cell

    def suppress(self, kp1: list, kp2: list, matches: list, image_shape: Tuple[int, int]) -> list:
        """
        Filters the matches list to ensure spatial uniformity across the source image.
        """
        if not matches:
            return []
            
        h, w = image_shape[:2]
        
        cell_h = h / self.grid_rows
        cell_w = w / self.grid_cols
        
        # Sort matches by distance (ascending) to keep best ones first
        sorted_matches = sorted(matches, key=lambda x: x.distance)
        
        # Grid to keep track of match count per cell
        grid_counts = np.zeros((self.grid_rows, self.grid_cols), dtype=int)
        
        filtered_matches = []
        
        for m in sorted_matches:
            # We base the grid on the source image keypoints
            pt = kp1[m.queryIdx].pt
            
            # Determine which cell the point falls into
            row_idx = int(pt[1] // cell_h)
            col_idx = int(pt[0] // cell_w)
            
            # Boundary safeguards
            row_idx = min(max(row_idx, 0), self.grid_rows - 1)
            col_idx = min(max(col_idx, 0), self.grid_cols - 1)
            
            if grid_counts[row_idx, col_idx] < self.max_per_cell:
                filtered_matches.append(m)
                grid_counts[row_idx, col_idx] += 1
                
        return filtered_matches
