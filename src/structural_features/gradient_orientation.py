import cv2
import numpy as np

class GradientOrientationExtractor:
    """
    Extracts dense gradient orientations to be used as invariant features
    against non-linear brightness shifts.
    """
    def __init__(self, ksize: int = 3):
        self.ksize = ksize
        
    def compute(self, image: np.ndarray) -> np.ndarray:
        """
        Computes the gradient orientation image normalized to [0, 255].
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Compute Scharr or Sobel gradients
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=self.ksize)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=self.ksize)
        
        # Calculate magnitude and angle
        mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
        
        # Normalize angle to 0-255 (0 to 360 degrees -> 0 to 255)
        angle_norm = (angle / 360.0) * 255.0
        
        # Mask out angles where magnitude is too low to be reliable
        mag_mask = mag > (np.max(mag) * 0.05)
        angle_norm = angle_norm * mag_mask
        
        return np.uint8(angle_norm)
