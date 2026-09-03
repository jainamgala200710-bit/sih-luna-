import cv2
import numpy as np
from typing import Tuple, Dict

class IlluminationSimulator:
    """
    Simulates variations in illumination typical for lunar surface images 
    (different solar azimuth/elevation angles).
    """
    def __init__(self, 
                 gamma_range: Tuple[float, float] = (0.5, 2.0),
                 contrast_range: Tuple[float, float] = (0.7, 1.3),
                 brightness_range: Tuple[int, int] = (-40, 40),
                 add_gradient: bool = True):
        self.gamma_range = gamma_range
        self.contrast_range = contrast_range
        self.brightness_range = brightness_range
        self.add_gradient = add_gradient

    def apply(self, image: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Applies non-linear illumination changes to the image.
        Returns the modified image and the parameters used.
        """
        img_float = image.astype(np.float32)
        h, w = image.shape[:2]
        
        # 1. Contrast and Brightness
        alpha = np.random.uniform(self.contrast_range[0], self.contrast_range[1])
        beta = np.random.randint(self.brightness_range[0], self.brightness_range[1])
        
        img_float = img_float * alpha + beta
        img_float = np.clip(img_float, 0, 255)
        
        # 2. Gamma correction (non-linear brightness shift)
        gamma = np.random.uniform(self.gamma_range[0], self.gamma_range[1])
        # Normalize to 0-1, apply gamma, scale back
        img_float = (img_float / 255.0) ** gamma * 255.0
        
        # 3. Simulate directional light (illumination gradient)
        gradient_intensity = 0.0
        gradient_angle = 0.0
        if self.add_gradient:
            gradient_intensity = np.random.uniform(0.1, 0.4)
            gradient_angle = np.random.uniform(0, 2 * np.pi)
            
            # Create linear gradient
            X, Y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
            gradient = X * np.cos(gradient_angle) + Y * np.sin(gradient_angle)
            # Normalize gradient to [1 - intensity, 1 + intensity]
            gradient = 1.0 + gradient * gradient_intensity
            
            # Apply gradient
            if len(image.shape) == 3:
                gradient = np.expand_dims(gradient, axis=2)
            img_float = img_float * gradient
            
        img_float = np.clip(img_float, 0, 255)
        result = img_float.astype(np.uint8)
        
        params = {
            "contrast_alpha": float(alpha),
            "brightness_beta": float(beta),
            "gamma": float(gamma),
            "gradient_intensity": float(gradient_intensity),
            "gradient_angle_rad": float(gradient_angle)
        }
        
        return result, params
