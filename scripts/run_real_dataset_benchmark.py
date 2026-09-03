import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import csv
import numpy as np
from src.matching.classical.feature_matching_pipeline import ClassicalMatchingPipeline
from src.subpixel.subpixel_refinement_pipeline import SubPixelRefinementPipeline
from src.transformation.model_validation_pipeline import ModelValidationPipeline

def run_benchmark(src_path, ref_path):
    source = cv2.imread(src_path)
    ref = cv2.imread(ref_path)
    
    if source is None or ref is None:
        return "FAILED", 0, "N/A"
        
    try:
        pipe = ClassicalMatchingPipeline('SIFT')
        kp1, kp2, matches = pipe.run_matching(source, ref)
        
        refiner = SubPixelRefinementPipeline()
        r_kp1, r_kp2, r_matches = refiner.refine_matches(source, ref, kp1, kp2, matches)
        
        val = ModelValidationPipeline()
        model_name, H, inlier_mask, rmse = val.select_transformation(r_kp1, r_kp2, r_matches)
        
        inliers_count = 0
        if inlier_mask is not None:
            inliers_count = int(np.sum(inlier_mask))
            
        return "SUCCESS" if H is not None else "FAILED", inliers_count, model_name
    except Exception as e:
        return f"ERROR: {str(e)}", 0, "N/A"

def benchmark_all():
    print("Running Extreme Modal Benchmarks...")
    results = []
    
    modes = [
        ("TMC2_vs_TMC2", "data/pairs/real/tmc2_tmc2/pair_001"),
        ("OHRC_vs_OHRC", "data/pairs/real/ohrc_ohrc/pair_001"),
        ("OHRC_vs_TMC2", "data/pairs/real/ohrc_tmc2/pair_001")
    ]
    
    for mode, path in modes:
        src = os.path.join(path, "source.png")
        ref = os.path.join(path, "reference.png")
        
        status, inliers, model = run_benchmark(src, ref)
        print(f"{mode}: {status} | Inliers: {inliers} | Best Model: {model}")
        
        results.append({
            "Modality": mode,
            "Status": status,
            "Inlier_Count": inliers,
            "Transformation_Model": model
        })
        
    os.makedirs("docs", exist_ok=True)
    with open("docs/REAL_DATA_PERFORMANCE.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Modality", "Status", "Inlier_Count", "Transformation_Model"])
        writer.writeheader()
        writer.writerows(results)
        
    print("Results dumped to docs/REAL_DATA_PERFORMANCE.csv")

if __name__ == "__main__":
    benchmark_all()
