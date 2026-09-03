import cv2
import numpy as np
from typing import List

from src.preprocessing.scale_pyramids import generate_gaussian_pyramid, generate_laplacian_pyramid

class PyramidBuilder:
    """
    Adapter leveraging Phase 8 ScalePyramids to explicitly generate
    scale-space structures for coarse-to-fine feature matching.
    """
    def __init__(self, levels: int = 4):
        self.levels = levels

    def build_gaussian_pyramid(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Builds a standard Gaussian pyramid where each successive image is
        downsampled by a factor of 2 (blur + decimate).
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        return generate_gaussian_pyramid(gray, self.levels)

    def build_laplacian_pyramid(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Builds a Laplacian pyramid capturing the high-frequency detail
        between successive Gaussian scales.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        return generate_laplacian_pyramid(gray, self.levels)
