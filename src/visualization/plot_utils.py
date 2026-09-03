import cv2
import numpy as np

def create_blended_overlay(img1: np.ndarray, img2: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """
    Creates a blended alpha overlay of two images of the same size.
    """
    assert img1.shape == img2.shape, f"Images must have same shape, got {img1.shape} and {img2.shape}"
    return cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)

def create_checkerboard(img1: np.ndarray, img2: np.ndarray, block_size: int = 50) -> np.ndarray:
    """
    Creates a checkerboard pattern alternating between img1 and img2.
    """
    assert img1.shape == img2.shape, f"Images must have same shape, got {img1.shape} and {img2.shape}"
    h, w = img1.shape[:2]
    
    # Create mask
    y, x = np.indices((h, w))
    checker = ((x // block_size) + (y // block_size)) % 2 == 0
    
    if len(img1.shape) == 3:
        checker = np.repeat(checker[:, :, np.newaxis], img1.shape[2], axis=2)
        
    result = np.where(checker, img1, img2)
    return result

def create_difference_image(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    """
    Creates an absolute difference image highlighting structural variations.
    """
    assert img1.shape == img2.shape, f"Images must have same shape, got {img1.shape} and {img2.shape}"
    return cv2.absdiff(img1, img2)
