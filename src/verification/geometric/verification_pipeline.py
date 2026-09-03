from typing import Dict, Any, Tuple
import numpy as np
from src.verification.geometric.ransac_homography import RANSACHomographyVerifier
from src.verification.geometric.usac_verifier import USACVerifier

class GeometricVerificationPipeline:
    """
    Central pipeline for filtering matches based on geometric consistency.
    """
    def __init__(self, method: str = 'USAC', config: Dict[str, Any] = None):
        self.method = method.upper()
        
        reproj = config.get('reproj_threshold', 3.0) if config else 3.0
        iters = config.get('max_iters', 2000) if config else 2000
        conf = config.get('confidence', 0.995) if config else 0.995
        
        if self.method == 'RANSAC':
            self.verifier = RANSACHomographyVerifier(reproj, iters, conf)
        elif self.method == 'USAC':
            # Boost iterations for USAC as it's faster/more robust
            self.verifier = USACVerifier(reproj, max(iters, 10000), max(conf, 0.999))
        else:
            raise ValueError(f"Unsupported verification method: {method}")

    def verify_matches(self, kp1: list, kp2: list, matches: list) -> Tuple[np.ndarray, list, dict]:
        """
        Executes verification and returns the computed transformation matrix,
        the filtered list of inlier matches, and a metric dictionary.
        """
        initial_count = len(matches)
        
        H, mask = self.verifier.verify(kp1, kp2, matches)
        inliers = self.verifier.extract_inliers(matches, mask)
        
        final_count = len(inliers)
        inlier_ratio = final_count / initial_count if initial_count > 0 else 0.0
        
        metrics = {
            "initial_matches": initial_count,
            "inlier_matches": final_count,
            "inlier_ratio": inlier_ratio,
            "matrix_computed": H is not None
        }
        
        return H, inliers, metrics
