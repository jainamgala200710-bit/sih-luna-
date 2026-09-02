import cv2
import numpy as np
import os
import shutil

def generate_noise(image, intensity=0.1):
    """Adds high-frequency Gaussian noise to simulate sensor degradation."""
    noise = np.random.normal(0, intensity * 255, image.shape).astype(np.float32)
    noisy = cv2.add(image.astype(np.float32), noise)
    return np.clip(noisy, 0, 255).astype(np.uint8)

def generate_illumination_gradient(image, direction='horizontal'):
    """Simulates drastic sun-angle variations across the orbital pass."""
    h, w = image.shape[:2]
    if direction == 'horizontal':
        gradient = np.tile(np.linspace(0.4, 1.2, w), (h, 1))
    else:
        gradient = np.tile(np.linspace(0.4, 1.2, h), (w, 1)).T
        
    if len(image.shape) == 3:
        gradient = np.dstack([gradient]*3)
        
    illuminated = image.astype(np.float32) * gradient
    return np.clip(illuminated, 0, 255).astype(np.uint8)

def create_proxy_datasets():
    print("Generating Proxy Real-World Data from Base Synthetics...")
    base_src = cv2.imread("data/synthetic/pair_001/source.png")
    base_ref = cv2.imread("data/synthetic/pair_001/reference.png")
    
    # Mode 1: TMC2 vs TMC2 (Same sensor, different pass, minor noise)
    dir_tmc2 = "data/pairs/real/tmc2_tmc2/pair_001"
    os.makedirs(dir_tmc2, exist_ok=True)
    cv2.imwrite(f"{dir_tmc2}/source.png", generate_noise(base_src, 0.05))
    cv2.imwrite(f"{dir_tmc2}/reference.png", base_ref)
    
    # Mode 2: OHRC vs OHRC (Same sensor, high resolution, structural rotation)
    dir_ohrc = "data/pairs/real/ohrc_ohrc/pair_001"
    os.makedirs(dir_ohrc, exist_ok=True)
    M = cv2.getRotationMatrix2D((400, 400), 15, 1.0) # 15 degree rotation
    rot_src = cv2.warpAffine(base_src, M, (800, 800))
    cv2.imwrite(f"{dir_ohrc}/source.png", generate_noise(rot_src, 0.15))
    cv2.imwrite(f"{dir_ohrc}/reference.png", base_ref)
    
    # Mode 3: OHRC vs TMC2 (Extreme Multi-Modal)
    # Drastic scale differential, extreme noise, severe illumination gradient
    dir_cross = "data/pairs/real/ohrc_tmc2/pair_001"
    os.makedirs(dir_cross, exist_ok=True)
    
    # Simulate 5m/px vs 0.25m/px (20x scale drop)
    # We'll do a 0.25x scale for mathematical feasibility in tests, representing a massive shift
    small_src = cv2.resize(base_src, (200, 200))
    noisy_src = generate_noise(small_src, 0.25)
    dark_src = generate_illumination_gradient(noisy_src, 'vertical')
    
    # The reference remains standard (representing the baseline map)
    cv2.imwrite(f"{dir_cross}/source.png", dark_src)
    cv2.imwrite(f"{dir_cross}/reference.png", base_ref)
    
    print("Proxy directories generated successfully.")

if __name__ == "__main__":
    create_proxy_datasets()
