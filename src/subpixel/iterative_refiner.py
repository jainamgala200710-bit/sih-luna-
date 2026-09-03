from src.subpixel.gradient_refinement import GradientRefinement
from src.subpixel.correlation_refinement import CorrelationRefinement
import numpy as np

class IterativeRefiner:
    """
    Orchestrates multiple refinement steps to ensure convergence.
    Combines both Gradient (cornerSubPix) and Correlation refinement.
    """
    def __init__(self):
        self.gradient_refiner = GradientRefinement()
        self.correlation_refiner = CorrelationRefinement()
        
    def refine(self, src_img: np.ndarray, ref_img: np.ndarray, kp1: list, kp2: list, matches: list):
        """
        Executes a two-pass refinement: first gradient-based local tuning on both images,
        followed by phase-correlation cross-tuning between the two images.
        """
        # Step 1: Self-Refinement via Gradients (cornerSubPix)
        grad_kp1 = self.gradient_refiner.refine(src_img, kp1)
        grad_kp2 = self.gradient_refiner.refine(ref_img, kp2)
        
        # Step 2: Cross-Refinement via Phase Correlation
        final_kp1, final_kp2 = self.correlation_refiner.refine(src_img, ref_img, grad_kp1, grad_kp2, matches)
        
        # To maintain the existing match indices in a simplified pipeline,
        # we rebuild a contiguous list of matched points since correlation_refiner
        # extracts out matched pairs directly.
        import cv2
        reindexed_matches = []
        for i in range(len(matches)):
            reindexed_matches.append(cv2.DMatch(i, i, matches[i].distance))
            
        return final_kp1, final_kp2, reindexed_matches
