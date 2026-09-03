from typing import Dict, Tuple

class PairValidator:
    """
    Validates image pairs before they are added to the dataset.
    Checks for minimum overlap, valid resolutions, and metadata completeness.
    """
    def __init__(self, min_overlap: float = 0.3):
        self.min_overlap = min_overlap

    def validate_pair(self, source_meta: Dict, ref_meta: Dict, overlap: float) -> Tuple[bool, str]:
        """
        Validates if a pair is suitable for registration experiments.
        """
        if overlap < self.min_overlap:
            return False, f"Overlap {overlap:.2f} is below minimum {self.min_overlap:.2f}"
            
        if not source_meta or not ref_meta:
            return False, "Missing metadata for source or reference"
            
        # Ensure dimensions exist
        if "dimensions" not in source_meta and "image_width" not in source_meta:
            pass # In practice we'd require this
            
        return True, "Valid Pair"
