import cv2
import numpy as np
import os

class OutlierVisualizer:
    """
    Visualizes inliers vs outliers after geometric verification.
    """
    def __init__(self, output_dir: str = "results/verification"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def visualize(self, img1: np.ndarray, kp1: list, img2: np.ndarray, kp2: list, matches: list, inliers: list, output_name: str) -> str:
        """
        Draws inliers in green and outliers in red.
        """
        inlier_set = set(inliers)
        
        # We need a custom drawing function to color lines differently
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        vis = np.zeros((max(h1, h2), w1 + w2, 3), dtype=np.uint8)
        
        if len(img1.shape) == 2:
            vis[:h1, :w1] = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        else:
            vis[:h1, :w1] = img1
            
        if len(img2.shape) == 2:
            vis[:h2, w1:w1+w2] = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        else:
            vis[:h2, w1:w1+w2] = img2
            
        # Draw outliers first (red) so inliers (green) are drawn on top
        for m in matches:
            if m not in inlier_set:
                pt1 = (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1]))
                pt2 = (int(kp2[m.trainIdx].pt[0]) + w1, int(kp2[m.trainIdx].pt[1]))
                cv2.line(vis, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
                
        # Draw inliers
        for m in inliers:
            pt1 = (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1]))
            pt2 = (int(kp2[m.trainIdx].pt[0]) + w1, int(kp2[m.trainIdx].pt[1]))
            cv2.line(vis, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.circle(vis, pt1, 3, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.circle(vis, pt2, 3, (0, 255, 0), 1, cv2.LINE_AA)
            
        out_path = os.path.join(self.output_dir, output_name)
        cv2.imwrite(out_path, vis)
        return out_path
