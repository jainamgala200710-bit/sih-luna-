from typing import Dict, Any, Tuple
import numpy as np

from src.matching.classical.feature_matching_pipeline import ClassicalMatchingPipeline
from src.verification.geometric.verification_pipeline import GeometricVerificationPipeline
from src.registration.image_warper import ImageWarper

class RegistrationPipeline:
    """
    End-to-end baseline registration pipeline combining classical feature matching,
    geometric verification, and image warping.
    """
    def __init__(self, matcher: str = 'SIFT', verifier: str = 'USAC', config: Dict[str, Any] = None):
        self.matcher = ClassicalMatchingPipeline(matcher, config)
        self.verifier = GeometricVerificationPipeline(verifier, config)
        self.warper = ImageWarper()
        
    def register(self, source_img: np.ndarray, ref_img: np.ndarray) -> Tuple[np.ndarray, np.ndarray, dict]:
        """
        Executes registration to align the source image to the reference image.
        Returns the computed homography, the warped image, and metrics.
        """
        # 1. Feature Matching
        kp1, kp2, matches = self.matcher.run_matching(source_img, ref_img)
        
        metrics = {
            "keypoints_source": len(kp1),
            "keypoints_ref": len(kp2),
            "raw_matches": len(matches)
        }
        
        if len(matches) < 4:
            metrics["status"] = "failed_insufficient_matches"
            return None, None, metrics
            
        # 2. Geometric Verification (Outlier Rejection)
        H, inliers, verif_metrics = self.verifier.verify_matches(kp1, kp2, matches)
        metrics.update(verif_metrics)
        
        if H is None:
            metrics["status"] = "failed_verification"
            return None, None, metrics
            
        # 3. Warping
        dsize = (ref_img.shape[1], ref_img.shape[0])
        warped_img = self.warper.warp_perspective(source_img, H, dsize)
        
        metrics["status"] = "success"
        
        return H, warped_img, metrics
