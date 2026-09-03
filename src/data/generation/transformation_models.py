import cv2
import numpy as np
from typing import Tuple, Dict

class GeometricTransformer:
    """
    Applies geometric transformations to simulate viewpoint variations.
    Returns the transformed image and the ground truth homography matrix.
    The ground truth homography H maps pixels from the source (transformed) image
    back to the reference (original) image.
    """
    def __init__(self, 
                 max_translation_pct: float = 0.1,
                 max_rotation_deg: float = 15.0,
                 scale_range: Tuple[float, float] = (0.8, 1.2),
                 max_perspective_distortion: float = 0.05):
        self.max_translation_pct = max_translation_pct
        self.max_rotation_deg = max_rotation_deg
        self.scale_range = scale_range
        self.max_perspective_distortion = max_perspective_distortion

    def transform(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, Dict]:
        """
        Applies a random geometric transformation to the image.
        Returns:
            transformed_image (np.ndarray): The transformed image.
            H (np.ndarray): 3x3 Homography matrix mapping source (transformed) to reference (original).
            params (Dict): Transformation parameters used.
        """
        h, w = image.shape[:2]
        
        # Random parameters
        tx = np.random.uniform(-self.max_translation_pct, self.max_translation_pct) * w
        ty = np.random.uniform(-self.max_translation_pct, self.max_translation_pct) * h
        angle = np.random.uniform(-self.max_rotation_deg, self.max_rotation_deg)
        scale = np.random.uniform(self.scale_range[0], self.scale_range[1])
        
        # Center of rotation
        center = (w / 2, h / 2)
        
        # 2x3 Affine transformation matrix (for rotation, scale, translation)
        # Note: cv2.getRotationMatrix2D maps from original to transformed
        M_affine = cv2.getRotationMatrix2D(center, angle, scale)
        M_affine[0, 2] += tx
        M_affine[1, 2] += ty
        
        # Convert to 3x3 Homography
        H_affine = np.eye(3)
        H_affine[0:2, :] = M_affine
        
        # Add perspective distortion
        src_points = np.float32([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]])
        
        # Jitter the corners
        dx = self.max_perspective_distortion * w
        dy = self.max_perspective_distortion * h
        dst_points = np.float32([
            [np.random.uniform(-dx, dx), np.random.uniform(-dy, dy)],
            [w-1 + np.random.uniform(-dx, dx), np.random.uniform(-dy, dy)],
            [np.random.uniform(-dx, dx), h-1 + np.random.uniform(-dy, dy)],
            [w-1 + np.random.uniform(-dx, dx), h-1 + np.random.uniform(-dy, dy)]
        ])
        
        # Perspective transform matrix
        H_perspective = cv2.getPerspectiveTransform(src_points, dst_points)
        
        # Combine transformations
        # H_total maps original to transformed
        H_total = H_perspective @ H_affine
        
        # Apply transformation
        transformed_image = cv2.warpPerspective(
            image, H_total, (w, h), 
            flags=cv2.INTER_LINEAR, 
            borderMode=cv2.BORDER_REFLECT_101
        )
        
        # Ground truth maps from transformed to original
        H_inv = np.linalg.inv(H_total)
        # Normalize homography
        H_inv /= H_inv[2, 2]
        
        params = {
            "translation_x": float(tx),
            "translation_y": float(ty),
            "rotation_deg": float(angle),
            "scale": float(scale),
            "perspective_distortion_max_pct": float(self.max_perspective_distortion)
        }
        
        return transformed_image, H_inv, params
