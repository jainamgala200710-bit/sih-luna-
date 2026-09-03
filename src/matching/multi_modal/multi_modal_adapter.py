import cv2
import numpy as np
from typing import Tuple

class MultiModalAdapter:
    """
    Standardizes cross-sensor / multi-modal imagery (e.g. OHRC vs LROC NAC)
    by matching histograms prior to feature extraction to minimize modality gaps.
    """
    def __init__(self):
        pass

    def adapt(self, source_img: np.ndarray, ref_img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Uses Histogram Matching to force the source image to adopt the tonal
        characteristics of the reference image, bridging the modality gap.
        """
        if len(source_img.shape) == 3:
            src_gray = cv2.cvtColor(source_img, cv2.COLOR_BGR2GRAY)
        else:
            src_gray = source_img.copy()
            
        if len(ref_img.shape) == 3:
            ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
        else:
            ref_gray = ref_img.copy()

        # Compute histograms and CDFs
        src_hist, _ = np.histogram(src_gray.flatten(), 256, [0, 256])
        ref_hist, _ = np.histogram(ref_gray.flatten(), 256, [0, 256])
        
        src_cdf = src_hist.cumsum()
        src_cdf_normalized = src_cdf / src_cdf.max()
        
        ref_cdf = ref_hist.cumsum()
        ref_cdf_normalized = ref_cdf / ref_cdf.max()
        
        # Create lookup table
        lookup_table = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            # Find the closest CDF value in reference
            diff = np.abs(ref_cdf_normalized - src_cdf_normalized[i])
            lookup_table[i] = np.argmin(diff)
            
        adapted_source = cv2.LUT(src_gray, lookup_table)
        
        return adapted_source, ref_gray
