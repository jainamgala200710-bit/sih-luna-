import numpy as np
import json
import os
from typing import Dict, Any

class BaselineEvaluator:
    """
    Evaluates the performance of feature matchers using ground truth transformations.
    Since geometric verification (RANSAC) is part of Phase 10, this evaluator
    relies purely on projecting source keypoints via the ground truth homography
    and calculating projection error distances to the matched reference keypoints.
    """
    def __init__(self, ground_truth_path: str):
        self.ground_truth_path = ground_truth_path
        with open(ground_truth_path, 'r') as f:
            self.gt = json.load(f)
            
        self.H = np.array(self.gt['homography'])
        
    def evaluate_matches(self, kp1: list, kp2: list, matches: list, inlier_threshold: float = 3.0) -> Dict[str, Any]:
        """
        Calculates precision based on ground truth projection.
        """
        if len(matches) == 0:
            return {"total_matches": 0, "correct_matches": 0, "precision": 0.0}
            
        correct_matches = 0
        
        for match in matches:
            # Get coordinates
            pt1 = np.array([kp1[match.queryIdx].pt])
            pt2 = np.array(kp2[match.trainIdx].pt)
            
            # Project pt1 using H
            pt1_h = np.array([pt1[0][0], pt1[0][1], 1.0])
            pt1_proj = np.dot(self.H, pt1_h)
            pt1_proj = pt1_proj[:2] / pt1_proj[2]
            
            # Calculate Euclidean distance
            dist = np.linalg.norm(pt1_proj - pt2)
            if dist <= inlier_threshold:
                correct_matches += 1
                
        precision = correct_matches / len(matches)
        
        return {
            "total_matches": len(matches),
            "correct_matches": correct_matches,
            "precision": precision
        }
