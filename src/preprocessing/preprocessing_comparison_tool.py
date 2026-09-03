import cv2
import numpy as np
import os
from src.preprocessing.preprocessing_pipeline import PreprocessingPipeline

class PreprocessingComparisonTool:
    """
    Compares raw and preprocessed images side-by-side.
    """
    def __init__(self, output_dir: str = "results/preprocessing_benchmarks"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def compare(self, image_path: str, config: dict = None) -> str:
        """
        Runs the pipeline on the image and saves a side-by-side comparison.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
            
        raw = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if raw is None:
            raise ValueError(f"Failed to read image: {image_path}")
            
        pipeline = PreprocessingPipeline(config)
        processed = pipeline.process(raw)
        
        # Ensure sizes and types match for display
        if len(raw.shape) == 2:
            raw_vis = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
        else:
            raw_vis = raw.copy()
            
        if len(processed.shape) == 2:
            proc_vis = cv2.cvtColor(processed.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        elif processed.dtype != np.uint8:
            proc_vis = cv2.normalize(processed, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        else:
            proc_vis = processed.copy()
            
        # Add labels
        cv2.putText(raw_vis, "Raw", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(proc_vis, "Processed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        comparison = np.hstack((raw_vis, proc_vis))
        
        filename = os.path.basename(image_path)
        out_path = os.path.join(self.output_dir, f"comparison_{filename}")
        cv2.imwrite(out_path, comparison)
        
        return out_path
