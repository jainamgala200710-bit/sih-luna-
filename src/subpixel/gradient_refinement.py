import cv2
import numpy as np
from typing import List, Tuple

class GradientRefinement:
    """
    Refines pixel-level correspondence coordinates to sub-pixel accuracy
    using OpenCV's cornerSubPix algorithm, which leverages local gradient
    approximations around the detected keypoints.
    """
    def __init__(self, win_size: Tuple[int, int] = (5, 5), max_iters: int = 100, eps: float = 0.001):
        self.win_size = win_size
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iters, eps)
        
    def refine(self, image: np.ndarray, keypoints: list) -> list:
        """
        Takes an image and a list of cv2.KeyPoint objects, returning 
        a new list of KeyPoints with sub-pixel refined coordinates.
        """
        if not keypoints:
            return []
            
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Convert keypoints to the format expected by cornerSubPix
        points = np.array([kp.pt for kp in keypoints], dtype=np.float32)
        
        # In-place sub-pixel refinement
        cv2.cornerSubPix(gray, points, self.win_size, (-1, -1), self.criteria)
        
        # Convert back to KeyPoint objects
        refined_keypoints = []
        for i, kp in enumerate(keypoints):
            refined_kp = cv2.KeyPoint(
                x=float(points[i][0]),
                y=float(points[i][1]),
                size=kp.size,
                angle=kp.angle,
                response=kp.response,
                octave=kp.octave,
                class_id=kp.class_id
            )
            refined_keypoints.append(refined_kp)
            
        return refined_keypoints
