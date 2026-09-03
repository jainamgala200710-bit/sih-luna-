from typing import Tuple, Dict, Any
import numpy as np
import cv2

from src.subpixel.iterative_refiner import IterativeRefiner

class SubPixelRefinementPipeline:
    """
    Pipeline integration component that takes coarsely matched keypoints and refines them
    to sub-pixel decimal coordinates to maximize homography geometric accuracy.
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.refiner = IterativeRefiner()
        
    def refine_matches(self, src_img: np.ndarray, ref_img: np.ndarray, kp1: list, kp2: list, matches: list) -> Tuple[list, list, list]:
        """
        Executes the iterative sub-pixel refinement engine.
        Returns newly generated KeyPoints and corresponding matches list.
        """
        if not matches:
            return kp1, kp2, matches
            
        refined_kp1, refined_kp2, refined_matches = self.refiner.refine(src_img, ref_img, kp1, kp2, matches)
        return refined_kp1, refined_kp2, refined_matches
