import json

class PipelineExhaustionError(Exception):
    """
    Custom exception raised when mathematical engines (like SIFT or RANSAC)
    physically exhaust their geometric capabilities, ensuring graceful degradation
    instead of crashing the backend in a C++ OpenCV fault.
    """
    def __init__(self, stage: str, reason: str, metadata: dict = None):
        self.stage = stage
        self.reason = reason
        self.metadata = metadata or {}
        
        super().__init__(f"Pipeline Exhaustion at '{stage}': {reason}")
        
    def to_dict(self):
        return {
            "status": "error",
            "error_type": "PipelineExhaustionError",
            "stage": self.stage,
            "message": self.reason,
            "metadata": self.metadata
        }
        
    def to_json(self):
        return json.dumps(self.to_dict())

def assert_minimum_matches(matches, minimum: int = 4, stage: str = "matching"):
    """
    Safeguards RANSAC requirements. RANSAC strictly requires N>=4 for homography.
    """
    if matches is None or len(matches) < minimum:
        raise PipelineExhaustionError(
            stage=stage,
            reason=f"Insufficient matching geometry (Found {len(matches) if matches else 0}, Minimum {minimum}). Classical extraction has failed.",
            metadata={"match_count": len(matches) if matches else 0, "minimum_required": minimum}
        )
