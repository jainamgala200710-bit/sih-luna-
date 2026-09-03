import numpy as np
import cv2
import json
import os
import logging
from typing import Dict, Any, List

from src.explainability.match_info_panel import MatchInfoPanel
from src.explainability.feature_similarity_visualizer import FeatureSimilarityVisualizer
from src.explainability.geometric_consistency_checker import GeometricConsistencyChecker
from src.explainability.refinement_visualizer import RefinementVisualizer
from src.explainability.uncertainty_visualizer import UncertaintyVisualizer

logger = logging.getLogger(__name__)

class ExplainabilityPipeline:
    """
    Wraps the various diagnostic and visualization components.
    Given a target match index, it triggers the entire explainability stack
    to generate a comprehensive human-readable dossier of exactly how and why
    the algorithm paired those two geometric coordinates.
    """
    def __init__(self, output_dir: str = "docs/reports/explainability"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.feat_vis = FeatureSimilarityVisualizer(output_dir)
        self.unc_vis = UncertaintyVisualizer(output_dir)
        
    def generate_dossier(self, src_img: np.ndarray, ref_img: np.ndarray,
                         kp1_list: list, kp2_list: list,
                         original_matches: list, target_match_idx: int,
                         H: np.ndarray = None,
                         refined_kp1_list: list = None, refined_kp2_list: list = None) -> Dict[str, Any]:
        """
        Builds the complete explainability dossier for a single specific match.
        """
        logger.info(f"Generating dossier for match index {target_match_idx} in session {self.output_dir}")
        if target_match_idx < 0 or target_match_idx >= len(original_matches):
            raise ValueError(f"Match index {target_match_idx} out of bounds.")

        m = original_matches[target_match_idx]
        kp1 = kp1_list[m.queryIdx]
        kp2 = kp2_list[m.trainIdx]

        dossier = {}

        # 1. Base Info
        logger.debug("Generating Match Information")
        dossier['Match Information'] = MatchInfoPanel.generate_info(m, kp1, kp2)

        # 2. Visual Patches
        logger.debug("Generating Feature Patch Visualization")
        patch_path = self.feat_vis.visualize_patch(src_img, ref_img, kp1, kp2, str(target_match_idx))
        dossier['Feature Patch Visualization'] = patch_path

        # 3. Geometric Consistency (If Homography provided)
        if H is not None:
            logger.debug("Generating Geometric Consistency")
            dossier['Geometric Consistency'] = GeometricConsistencyChecker.analyze_match(kp1, kp2, H)

        # 4. Refinement (If refined lists provided)
        if refined_kp1_list is not None and refined_kp2_list is not None:
            logger.debug("Generating Refinement visualizations")
            rkp1 = refined_kp1_list[target_match_idx]
            rkp2 = refined_kp2_list[target_match_idx]

            dossier['Source Point Refinement'] = RefinementVisualizer.explain_refinement(kp1, rkp1)
            dossier['Target Point Refinement'] = RefinementVisualizer.explain_refinement(kp2, rkp2)

        # 5. Uncertainty
        logger.debug("Generating Uncertainty visualizations")
        unc_src_path = self.unc_vis.visualize_uncertainty(src_img, kp1, f"{target_match_idx}_src")
        unc_ref_path = self.unc_vis.visualize_uncertainty(ref_img, kp2, f"{target_match_idx}_ref")

        dossier['Source Uncertainty Visualization'] = unc_src_path
        dossier['Reference Uncertainty Visualization'] = unc_ref_path

        # Save to JSON
        json_path = os.path.join(self.output_dir, f"dossier_{target_match_idx}.json")
        logger.debug(f"Saving dossier to {json_path}")
        with open(json_path, 'w') as f:
            json.dump(dossier, f, indent=4)

        logger.info(f"Dossier generated successfully for match index {target_match_idx}")
        return dossier
