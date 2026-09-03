import cv2
import numpy as np

def min_max_normalize(image: np.ndarray, target_min: float = 0.0, target_max: float = 255.0) -> np.ndarray:
    """Linearly normalizes image intensities to a specific range."""
    img_min = image.min()
    img_max = image.max()
    
    if img_max == img_min:
        return np.ones_like(image, dtype=np.float32) * target_min
        
    normalized = (image - img_min) / (img_max - img_min)
    return (normalized * (target_max - target_min) + target_min).astype(image.dtype)

def z_score_normalize(image: np.ndarray) -> np.ndarray:
    """Normalizes image to have zero mean and unit variance."""
    mean = np.mean(image)
    std = np.std(image)
    
    if std == 0:
        return np.zeros_like(image, dtype=np.float32)
        
    return (image.astype(np.float32) - mean) / std
