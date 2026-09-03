import cv2
import numpy as np

class StructuralEdgeExtractor:
    """
    Extracts structural edge maps invariant to absolute pixel intensities.
    Useful as an image representation prior to feature detection.
    """
    def __init__(self, method: str = 'canny', lower_thresh: int = 50, upper_thresh: int = 150):
        self.method = method.lower()
        self.lower_thresh = lower_thresh
        self.upper_thresh = upper_thresh
        
    def compute(self, image: np.ndarray) -> np.ndarray:
        """
        Computes the structural edge map based on the selected method.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Light Gaussian blur to denoise prior to edge detection
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
        if self.method == 'canny':
            edges = cv2.Canny(blurred, self.lower_thresh, self.upper_thresh)
            return edges
        elif self.method == 'laplacian':
            edges = cv2.Laplacian(blurred, cv2.CV_64F)
            edges = cv2.convertScaleAbs(edges)
            return edges
        else:
            raise ValueError(f"Unknown edge extraction method: {self.method}")
