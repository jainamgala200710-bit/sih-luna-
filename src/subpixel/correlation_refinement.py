import cv2
import numpy as np
from typing import Tuple

class CorrelationRefinement:
    """
    Refines feature matches by extracting a local window around the keypoint in the
    source image and performing sub-pixel template matching via Phase Correlation
    against the corresponding neighborhood in the reference image.
    """
    def __init__(self, window_size: int = 21):
        self.window_size = window_size
        self.half_win = window_size // 2
        
    def refine(self, src_img: np.ndarray, ref_img: np.ndarray, kp1: list, kp2: list, matches: list) -> Tuple[list, list]:
        """
        Adjusts kp2 based on phase correlation offsets relative to kp1.
        Returns the refined lists of kp1 and kp2.
        """
        if len(src_img.shape) == 3:
            src_gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
            ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
        else:
            src_gray = src_img
            ref_gray = ref_img
            
        src_gray = np.float32(src_gray)
        ref_gray = np.float32(ref_gray)
        
        refined_kp1 = []
        refined_kp2 = []
        
        h, w = src_gray.shape
        
        for m in matches:
            pt1 = kp1[m.queryIdx].pt
            pt2 = kp2[m.trainIdx].pt
            
            x1, y1 = int(pt1[0]), int(pt1[1])
            x2, y2 = int(pt2[0]), int(pt2[1])
            
            # Boundary checks
            if (x1 - self.half_win < 0 or x1 + self.half_win >= w or
                y1 - self.half_win < 0 or y1 + self.half_win >= h or
                x2 - self.half_win < 0 or x2 + self.half_win >= w or
                y2 - self.half_win < 0 or y2 + self.half_win >= h):
                
                # Keep original if window falls off edge
                refined_kp1.append(kp1[m.queryIdx])
                refined_kp2.append(kp2[m.trainIdx])
                continue
                
            # Extract patches
            patch1 = src_gray[y1-self.half_win:y1+self.half_win+1, x1-self.half_win:x1+self.half_win+1]
            patch2 = ref_gray[y2-self.half_win:y2+self.half_win+1, x2-self.half_win:x2+self.half_win+1]
            
            # Perform phase correlation to find sub-pixel shift
            shift, _ = cv2.phaseCorrelate(patch1, patch2)
            
            # Create new keypoint for ref_img adjusted by the sub-pixel shift
            orig_kp = kp2[m.trainIdx]
            refined_kp = cv2.KeyPoint(
                x=float(orig_kp.pt[0] - shift[0]),
                y=float(orig_kp.pt[1] - shift[1]),
                size=orig_kp.size,
                angle=orig_kp.angle,
                response=orig_kp.response,
                octave=orig_kp.octave,
                class_id=orig_kp.class_id
            )
            
            refined_kp1.append(kp1[m.queryIdx])
            refined_kp2.append(refined_kp)
            
        return refined_kp1, refined_kp2
