import cv2
import numpy as np

class PhaseCongruencyEngine:
    """
    Computes Phase Congruency, an illumination and contrast invariant measure of image structure.
    Approximated using a bank of Log-Gabor filters across multiple orientations and scales.
    """
    def __init__(self, scales: int = 4, orientations: int = 6):
        self.scales = scales
        self.orientations = orientations
        
    def compute(self, image: np.ndarray) -> np.ndarray:
        """
        Approximates phase congruency using OpenCV's Gabor kernels.
        Full Log-Gabor requires custom frequency domain filtering, so we use
        a multi-scale spatial Gabor approach which is highly effective for edges.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        gray = np.float32(gray) / 255.0
        
        # Accumulate energy and amplitude
        total_energy = np.zeros_like(gray)
        total_amplitude = np.zeros_like(gray)
        
        # We iterate over multiple scales and orientations
        for s in range(self.scales):
            wavelength = 3.0 * (2.1 ** s) 
            sigma = 0.65 * wavelength
            
            for o in range(self.orientations):
                theta = o * np.pi / self.orientations
                
                # Real (even) and Imaginary (odd) Gabor filters
                k_real = cv2.getGaborKernel((int(sigma*4), int(sigma*4)), sigma, theta, wavelength, 1.0, 0, ktype=cv2.CV_32F)
                k_imag = cv2.getGaborKernel((int(sigma*4), int(sigma*4)), sigma, theta, wavelength, 1.0, np.pi/2, ktype=cv2.CV_32F)
                
                resp_real = cv2.filter2D(gray, cv2.CV_32F, k_real)
                resp_imag = cv2.filter2D(gray, cv2.CV_32F, k_imag)
                
                amplitude = np.sqrt(resp_real**2 + resp_imag**2)
                energy = resp_real # Approximation of local energy
                
                total_amplitude += amplitude
                total_energy += np.maximum(energy, 0)
                
        # Phase congruency is Energy / (Amplitude + epsilon)
        epsilon = 0.0001
        pc = total_energy / (total_amplitude + epsilon)
        
        # Normalize to 0-255 uint8 for easy OpenCV usage
        pc = cv2.normalize(pc, None, 0, 255, cv2.NORM_MINMAX)
        return np.uint8(pc)
