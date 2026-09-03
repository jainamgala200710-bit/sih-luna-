import matplotlib.pyplot as plt
import os
from typing import Dict, Any

class EvaluationVisualizer:
    """
    Renders bar charts and scatter plots analyzing comparative performance
    across different algorithms or configurations.
    """
    def __init__(self, output_dir: str = "docs/reports/graphs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def plot_metric_comparison(self, comparison_data: Dict[str, Any], metric: str, title: str, output_name: str):
        """
        Plots a side-by-side comparison of a single metric.
        """
        baseline_val = comparison_data[metric]['baseline']
        target_val = comparison_data[metric]['target']
        
        labels = ['Baseline', 'Target']
        values = [baseline_val, target_val]
        
        plt.figure(figsize=(8, 6))
        bars = plt.bar(labels, values, color=['#7f8c8d', '#2980b9'])
        
        plt.title(title)
        plt.ylabel(metric.upper() + ' (Pixels)')
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.3f}', ha='center', va='bottom')
            
        plt.tight_layout()
        out_path = os.path.join(self.output_dir, output_name)
        plt.savefig(out_path)
        plt.close()
