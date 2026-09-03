import numpy as np
from typing import Dict, Any

from src.preprocessing.normalization import min_max_normalize, z_score_normalize
from src.preprocessing.contrast_enhancement import apply_clahe, apply_histogram_equalization
from src.preprocessing.noise_reduction import apply_gaussian_blur, apply_median_blur, apply_bilateral_filter
from src.preprocessing.feature_extractors import compute_phase_congruency

class PreprocessingPipeline:
    """
    Configurable preprocessing pipeline for lunar imagery.
    """
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            self.config = {
                "noise_reduction": "gaussian", # gaussian, median, bilateral, none
                "noise_reduction_kernel": 5,
                "contrast_enhancement": "clahe", # clahe, hist_eq, none
                "clahe_clip_limit": 2.0,
                "normalization": "min_max", # min_max, z_score, none
                "extract_structure": False
            }
        else:
            self.config = config
            
    def process(self, image: np.ndarray) -> np.ndarray:
        """Applies configured preprocessing steps to the image sequentially."""
        processed = image.copy()
        
        # 1. Noise Reduction
        if self.config.get("noise_reduction") == "gaussian":
            k = self.config.get("noise_reduction_kernel", 5)
            processed = apply_gaussian_blur(processed, (k, k))
        elif self.config.get("noise_reduction") == "median":
            k = self.config.get("noise_reduction_kernel", 5)
            processed = apply_median_blur(processed, k)
        elif self.config.get("noise_reduction") == "bilateral":
            processed = apply_bilateral_filter(processed)
            
        # 2. Contrast Enhancement
        if self.config.get("contrast_enhancement") == "clahe":
            clip = self.config.get("clahe_clip_limit", 2.0)
            processed = apply_clahe(processed, clip_limit=clip)
        elif self.config.get("contrast_enhancement") == "hist_eq":
            processed = apply_histogram_equalization(processed)
            
        # 3. Structural Extraction (Optional, useful for illumination invariance)
        if self.config.get("extract_structure"):
            processed = compute_phase_congruency(processed)
            
        # 4. Normalization
        if self.config.get("normalization") == "min_max":
            processed = min_max_normalize(processed)
        elif self.config.get("normalization") == "z_score":
            processed = z_score_normalize(processed)
            
        return processed
