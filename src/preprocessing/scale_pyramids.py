import cv2
import numpy as np
from typing import List

def generate_gaussian_pyramid(image: np.ndarray, levels: int = 3) -> List[np.ndarray]:
    """
    Generates a Gaussian pyramid for multi-scale analysis.
    """
    pyramid = [image]
    for i in range(1, levels):
        pyramid.append(cv2.pyrDown(pyramid[i-1]))
    return pyramid

def generate_laplacian_pyramid(image: np.ndarray, levels: int = 3) -> List[np.ndarray]:
    """
    Generates a Laplacian pyramid which captures high-frequency structural details at multiple scales.
    """
    gaussian_pyr = generate_gaussian_pyramid(image, levels + 1)
    laplacian_pyr = []
    
    for i in range(levels):
        size = (gaussian_pyr[i].shape[1], gaussian_pyr[i].shape[0])
        expanded = cv2.pyrUp(gaussian_pyr[i+1], dstsize=size)
        laplacian = cv2.subtract(gaussian_pyr[i], expanded)
        laplacian_pyr.append(laplacian)
        
    return laplacian_pyr
