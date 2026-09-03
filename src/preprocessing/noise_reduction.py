import cv2
import numpy as np

def apply_gaussian_blur(image: np.ndarray, kernel_size: tuple = (5, 5), sigma: float = 0) -> np.ndarray:
    """Applies Gaussian blur to reduce high-frequency noise."""
    return cv2.GaussianBlur(image, kernel_size, sigma)

def apply_median_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Applies median blur, useful for removing salt-and-pepper noise."""
    # OpenCV's medianBlur requires odd kernel size
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.medianBlur(image.astype(np.uint8), kernel_size)

def apply_bilateral_filter(image: np.ndarray, d: int = 9, sigma_color: float = 75, sigma_space: float = 75) -> np.ndarray:
    """Applies bilateral filtering which reduces noise while preserving edges."""
    return cv2.bilateralFilter(image.astype(np.uint8), d, sigma_color, sigma_space)
