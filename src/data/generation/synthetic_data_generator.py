import os
import cv2
import json
import numpy as np
from typing import Dict, Any

from src.data.generation.transformation_models import GeometricTransformer
from src.data.generation.illumination_models import IlluminationSimulator

class SyntheticLunarGenerator:
    """
    Generates synthetic lunar dataset pairs with known ground truth transformations.
    """
    def __init__(self, output_dir: str = "data/synthetic"):
        self.output_dir = output_dir
        self.transformer = GeometricTransformer()
        self.illuminator = IlluminationSimulator()
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_base_image(self, size: int = 512) -> np.ndarray:
        """Generates a procedural image resembling a rough lunar surface with craters."""
        # Start with perlin-like noise (we'll approximate with blurred random noise)
        base = np.random.normal(128, 30, (size, size)).astype(np.float32)
        base = cv2.GaussianBlur(base, (15, 15), 0)
        
        # Add high frequency noise
        high_freq = np.random.normal(0, 10, (size, size)).astype(np.float32)
        base += high_freq
        
        # Draw random craters
        num_craters = np.random.randint(20, 50)
        for _ in range(num_craters):
            x = np.random.randint(0, size)
            y = np.random.randint(0, size)
            r = np.random.randint(5, 40)
            
            # Crater rim
            cv2.circle(base, (x, y), r, (180,), 2, cv2.LINE_AA)
            # Crater shadow inside (simple approximation)
            cv2.circle(base, (x-int(r*0.2), y-int(r*0.2)), int(r*0.8), (70,), -1, cv2.LINE_AA)
            
        base = np.clip(base, 0, 255).astype(np.uint8)
        # Convert to 3 channel for standard handling, though it's grayscale
        base = cv2.cvtColor(base, cv2.COLOR_GRAY2BGR)
        return base

    def generate_pair(self, pair_id: str) -> bool:
        """Generates a single synthetic pair and saves it to disk."""
        pair_dir = os.path.join(self.output_dir, pair_id)
        os.makedirs(pair_dir, exist_ok=True)
        
        # 1. Base Image (Reference)
        reference_img = self.generate_base_image()
        
        # 2. Geometric Transformation
        source_img, homography_matrix, geo_params = self.transformer.transform(reference_img)
        
        # 3. Illumination Variation
        source_img, ill_params = self.illuminator.apply(source_img)
        
        # 4. Add Degradation (Noise and blur)
        # Blur
        blur_kernel = np.random.choice([3, 5])
        source_img = cv2.GaussianBlur(source_img, (blur_kernel, blur_kernel), 0)
        # Noise
        noise = np.random.normal(0, 5, source_img.shape).astype(np.float32)
        source_img = np.clip(source_img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        
        # Save Images
        cv2.imwrite(os.path.join(pair_dir, "reference.png"), reference_img)
        cv2.imwrite(os.path.join(pair_dir, "source.png"), source_img)
        
        # Save Ground Truth
        ground_truth = {
            "homography": homography_matrix.tolist()
        }
        with open(os.path.join(pair_dir, "ground_truth.json"), "w") as f:
            json.dump(ground_truth, f, indent=4)
            
        # Save Metadata
        metadata = {
            "pair_id": pair_id,
            "geometric_parameters": geo_params,
            "illumination_parameters": ill_params,
            "degradation": {
                "blur_kernel": int(blur_kernel),
                "noise_sigma": 5.0
            }
        }
        with open(os.path.join(pair_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)
            
        return True

    def generate_dataset(self, num_pairs: int = 20):
        """Generates a complete dataset of image pairs."""
        print(f"Generating {num_pairs} synthetic lunar image pairs...")
        for i in range(1, num_pairs + 1):
            pair_id = f"pair_{i:03d}"
            self.generate_pair(pair_id)
            print(f"  - Generated {pair_id}")
        print(f"Dataset generated at: {self.output_dir}")

if __name__ == "__main__":
    generator = SyntheticLunarGenerator()
    generator.generate_dataset(20)
