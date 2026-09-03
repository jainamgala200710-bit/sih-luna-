import cv2
import numpy as np
from typing import Dict

def compute_sharpness(img: np.ndarray) -> float:
    """Computes image sharpness using variance of the Laplacian."""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())

def compute_contrast(img: np.ndarray) -> float:
    """Computes RMS contrast of the image."""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return float(np.std(gray))

def compute_brightness(img: np.ndarray) -> float:
    """Computes average brightness of the image."""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return float(np.mean(gray))

class QualityAssessor:
    """
    Computes quality metrics for a dataset.
    """
    def __init__(self):
        pass
        
    def assess_image(self, img: np.ndarray) -> Dict[str, float]:
        """Returns a dictionary of quality metrics for an image."""
        return {
            "sharpness": compute_sharpness(img),
            "contrast": compute_contrast(img),
            "brightness": compute_brightness(img)
        }
        
    def assess_pair(self, source: np.ndarray, reference: np.ndarray) -> Dict[str, float]:
        """Returns a comparative assessment between a pair."""
        s_metrics = self.assess_image(source)
        r_metrics = self.assess_image(reference)
        
        return {
            "source_sharpness": s_metrics["sharpness"],
            "reference_sharpness": r_metrics["sharpness"],
            "sharpness_ratio": s_metrics["sharpness"] / (r_metrics["sharpness"] + 1e-6),
            "contrast_difference": abs(s_metrics["contrast"] - r_metrics["contrast"]),
            "brightness_difference": abs(s_metrics["brightness"] - r_metrics["brightness"])
        }
