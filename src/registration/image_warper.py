import cv2
import numpy as np

class ImageWarper:
    """
    Handles geometric transformations to warp images based on computed matrices.
    """
    def __init__(self):
        pass

    def warp_perspective(self, image: np.ndarray, H: np.ndarray, dsize: tuple) -> np.ndarray:
        """
        Warps an image using a homography matrix.
        """
        if H is None:
            raise ValueError("Homography matrix cannot be None")
        
        # We use CUBIC interpolation for better quality on scientific images
        return cv2.warpPerspective(image, H, dsize, flags=cv2.INTER_CUBIC)
        
    def overlay_images(self, base_img: np.ndarray, warped_img: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        """
        Creates a blended overlay to visually verify registration.
        """
        if base_img.shape != warped_img.shape:
            raise ValueError("Images must have the same shape for overlay")
            
        if len(base_img.shape) == 2:
            base_img = cv2.cvtColor(base_img, cv2.COLOR_GRAY2BGR)
        if len(warped_img.shape) == 2:
            warped_img = cv2.cvtColor(warped_img, cv2.COLOR_GRAY2BGR)
            
        return cv2.addWeighted(base_img, alpha, warped_img, 1.0 - alpha, 0)
