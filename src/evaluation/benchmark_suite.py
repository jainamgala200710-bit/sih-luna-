import os
import json
import cv2
import numpy as np
from typing import Dict, Any, Callable

class BenchmarkSuite:
    """
    Automated testing framework running specific algorithms against all pairs
    in a synthetic dataset, aggregating the geometric performance metrics.
    """
    def __init__(self, dataset_path: str = "data/synthetic"):
        self.dataset_path = dataset_path
        
    def run_suite(self, pipeline_func: Callable[[np.ndarray, np.ndarray], np.ndarray]) -> Dict[str, Any]:
        """
        Executes the provided full pipeline function against all dataset pairs.
        The `pipeline_func` must take (source_img, reference_img) and return the 
        predicted Homography Matrix (H).
        """
        from src.evaluation.registration_metrics import RegistrationMetrics
        results = {}
        
        pair_dirs = [d for d in os.listdir(self.dataset_path) if os.path.isdir(os.path.join(self.dataset_path, d))]
        
        for pair in pair_dirs:
            pair_path = os.path.join(self.dataset_path, pair)
            
            source_path = os.path.join(pair_path, "source.png")
            ref_path = os.path.join(pair_path, "reference.png")
            gt_path = os.path.join(pair_path, "ground_truth.json")
            
            if not (os.path.exists(source_path) and os.path.exists(ref_path) and os.path.exists(gt_path)):
                continue
                
            src = cv2.imread(source_path)
            ref = cv2.imread(ref_path)
            
            with open(gt_path, 'r') as f:
                gt_data = json.load(f)
                gt_H = np.array(gt_data['homography'])
                
            try:
                # Execute pipeline to get predicted H
                pred_H = pipeline_func(src, ref)
                
                # We need source points and reference points to calculate RMSE. 
                # For a pure benchmark suite lacking internal pipeline access, we can synthesize them
                # by randomly sampling points from the source image and warping them using gt_H
                h, w = src.shape[:2]
                sample_pts = np.random.rand(100, 2) * np.array([w, h])
                pts_src = sample_pts.astype(np.float32)
                pts_ref = cv2.perspectiveTransform(pts_src.reshape(-1, 1, 2), gt_H).reshape(-1, 2)
                
                metrics = RegistrationMetrics.full_evaluation(pts_src, pts_ref, pred_H, gt_H, src.shape)
                results[pair] = metrics
                
            except Exception as e:
                results[pair] = {"error": str(e)}
                
        return results
