import cv2
import numpy as np
from typing import Dict, Any

class MatchInfoPanel:
    """
    Constructs a textual summary rendering localized metadata for a specific match.
    Provides diagnostic transparency into the pipeline's decision-making on a per-feature basis.
    """
    @staticmethod
    def generate_info(m: cv2.DMatch, kp1: cv2.KeyPoint, kp2: cv2.KeyPoint, status: str = "Accepted") -> Dict[str, Any]:
        """
        Extracts mathematical metrics from the OpenCV structures into human-readable telemetry.
        """
        info = {
            "Match ID": f"{m.queryIdx} -> {m.trainIdx}",
            "Status": status,
            "Source Coordinates (x,y)": (round(kp1.pt[0], 3), round(kp1.pt[1], 3)),
            "Reference Coordinates (x,y)": (round(kp2.pt[0], 3), round(kp2.pt[1], 3)),
            "Descriptor Distance": round(m.distance, 4),
            "Source Scale (Size)": round(kp1.size, 2),
            "Reference Scale (Size)": round(kp2.size, 2),
            "Scale Ratio (Ref/Src)": round(kp2.size / kp1.size, 3) if kp1.size > 0 else 0,
            "Source Angle": round(kp1.angle, 1),
            "Reference Angle": round(kp2.angle, 1),
            "Angle Difference": round(abs(kp1.angle - kp2.angle), 1)
        }
        return info
        
    @staticmethod
    def print_panel(info: Dict[str, Any]):
        """Prints the info panel to the console."""
        print("-" * 40)
        print("MATCH EXPLAINABILITY PANEL")
        print("-" * 40)
        for k, v in info.items():
            print(f"{k}: {v}")
        print("-" * 40)
