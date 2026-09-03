import cv2
import numpy as np
from typing import Tuple, List, Dict

class LoFTRMatcher:
    """
    Implements deep learning correspondence matching using Kornia's LoFTR.
    Local Feature TRansformer (LoFTR) is a detector-free matcher that produces
    semi-dense matches at a coarse level and refines them at a fine level.
    """
    def __init__(self, pretrained: str = 'outdoor', confidence_threshold: float = 0.2):
        self.confidence_threshold = confidence_threshold
        
        try:
            import torch
            import kornia.feature as kf
        except ImportError:
            raise ImportError(
                "PyTorch and Kornia are required for Deep Learning matchers. "
                "Please install them via: py -m pip install torch torchvision kornia"
            )
            
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load pre-trained LoFTR model from Kornia
        self.matcher = kf.LoFTR(pretrained=pretrained)
        self.matcher = self.matcher.to(self.device).eval()

    def match(self, img1: np.ndarray, img2: np.ndarray) -> Tuple[List[cv2.KeyPoint], List[cv2.KeyPoint], List[cv2.DMatch]]:
        """
        Matches img1 and img2 using LoFTR.
        Returns OpenCV-compatible Keypoints and DMatches for seamless integration.
        """
        import torch
        
        # Preprocess images to grayscale tensors
        if len(img1.shape) == 3:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        else:
            gray1 = img1
            
        if len(img2.shape) == 3:
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        else:
            gray2 = img2
            
        # Convert to torch tensor [B, C, H, W], normalized to [0, 1]
        tensor1 = torch.from_numpy(gray1)[None, None].float().to(self.device) / 255.0
        tensor2 = torch.from_numpy(gray2)[None, None].float().to(self.device) / 255.0
        
        input_dict = {"image0": tensor1, "image1": tensor2}
        
        with torch.no_grad():
            correspondences = self.matcher(input_dict)
            
        # correspondences contains 'keypoints0', 'keypoints1', 'confidence'
        mkpts0 = correspondences['keypoints0'].cpu().numpy()
        mkpts1 = correspondences['keypoints1'].cpu().numpy()
        conf = correspondences['confidence'].cpu().numpy()
        
        # Filter by confidence
        mask = conf > self.confidence_threshold
        mkpts0 = mkpts0[mask]
        mkpts1 = mkpts1[mask]
        conf = conf[mask]
        
        # Convert to OpenCV objects
        kp1 = []
        kp2 = []
        matches = []
        
        for i, (pt0, pt1, c) in enumerate(zip(mkpts0, mkpts1, conf)):
            kp1.append(cv2.KeyPoint(x=float(pt0[0]), y=float(pt0[1]), size=1.0))
            kp2.append(cv2.KeyPoint(x=float(pt1[0]), y=float(pt1[1]), size=1.0))
            
            # DMatch(queryIdx, trainIdx, distance). 
            # We use (1 - confidence) as distance so higher confidence = lower distance
            matches.append(cv2.DMatch(i, i, 1.0 - float(c)))
            
        return kp1, kp2, matches
