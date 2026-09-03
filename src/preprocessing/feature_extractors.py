import cv2
import numpy as np
from scipy import fftpack

def compute_gradients(image: np.ndarray) -> tuple:
    """Computes Sobel gradients for edge detection."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    
    magnitude, angle = cv2.cartToPolar(grad_x, grad_y, angleInDegrees=True)
    return magnitude, angle

def compute_phase_congruency(image: np.ndarray) -> np.ndarray:
    """
    Computes a simplified Phase Congruency map.
    Phase congruency is highly invariant to illumination changes,
    making it ideal for lunar imagery captured under different lighting.
    Note: A full implementation (like Kovesi's) requires multiple scales and orientations.
    This is a simplified frequency-domain structural representation placeholder.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    else:
        gray = image.astype(np.float32)
        
    # Standardize
    gray = (gray - np.mean(gray)) / (np.std(gray) + 1e-6)
    
    # 2D FFT
    F = fftpack.fft2(gray)
    F_shifted = fftpack.fftshift(F)
    
    # Magnitude and Phase
    magnitude = np.abs(F_shifted)
    
    # High-pass filter to emphasize structure over smooth gradients
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols), np.uint8)
    r = 30
    cv2.circle(mask, (ccol, crow), r, 0, -1)
    
    F_filtered = F_shifted * mask
    
    # IFFT back
    F_inv_shift = fftpack.ifftshift(F_filtered)
    img_back = fftpack.ifft2(F_inv_shift)
    img_back = np.abs(img_back)
    
    # Normalize to 0-255
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return img_back
