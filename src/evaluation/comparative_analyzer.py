from typing import Dict, Any, List

class ComparativeAnalyzer:
    """
    Analyzes and compares the results of multiple algorithmic configurations
    (e.g., Baseline SIFT vs Multi-Scale Phase-Congruency SIFT).
    """
    def __init__(self):
        self.experiments = {}

    def log_experiment(self, name: str, metrics: Dict[str, float]):
        """Logs a completed run into memory."""
        self.experiments[name] = metrics

    def get_baseline_comparison(self, baseline_name: str, target_name: str) -> Dict[str, Any]:
        """
        Computes the relative delta (improvement or degradation) between
        an advanced pipeline and the defined baseline.
        """
        if baseline_name not in self.experiments or target_name not in self.experiments:
            raise ValueError("One or both experiment names not found in memory.")
            
        base = self.experiments[baseline_name]
        target = self.experiments[target_name]
        
        comparison = {}
        for key in base.keys():
            if key in target:
                # Lower is generally better for our metrics (RMSE, TRE)
                # A negative delta means the target is lower (improved)
                delta = target[key] - base[key]
                pct_change = (delta / base[key]) * 100 if base[key] != 0 else 0
                comparison[key] = {
                    "baseline": base[key],
                    "target": target[key],
                    "delta": delta,
                    "improvement_percent": -pct_change # Positive means improved
                }
                
        return comparison
