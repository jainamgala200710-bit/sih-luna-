import os
import json
from typing import Dict, Any

class AutoReportGenerator:
    """
    Automates the translation of benchmark JSON metrics into human-readable 
    Markdown reports for engineering review.
    """
    def __init__(self, output_dir: str = "docs/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_report(self, report_name: str, config_name: str, metrics: Dict[str, Any]) -> str:
        """
        Creates a markdown report summarizing the benchmark.
        """
        filepath = os.path.join(self.output_dir, f"{report_name}.md")
        
        with open(filepath, 'w') as f:
            f.write(f"# Benchmark Report: {config_name}\n\n")
            f.write("## Overview\n")
            f.write("Automated evaluation of pipeline performance across synthetic datasets.\n\n")
            
            f.write("## Results per Pair\n")
            
            success_count = 0
            total_rmse = 0.0
            total_tre = 0.0
            
            for pair, data in metrics.items():
                if "error" in data:
                    f.write(f"- **{pair}**: FAILED ({data['error']})\n")
                else:
                    f.write(f"- **{pair}**: RMSE = {data['rmse']:.3f}, TRE = {data['tre']:.3f}\n")
                    success_count += 1
                    total_rmse += data['rmse']
                    total_tre += data['tre']
                    
            f.write("\n## Aggregate Metrics\n")
            f.write(f"- **Total Pairs Processed**: {len(metrics)}\n")
            f.write(f"- **Successful Registrations**: {success_count}\n")
            
            if success_count > 0:
                f.write(f"- **Mean RMSE**: {total_rmse / success_count:.3f} px\n")
                f.write(f"- **Mean TRE**: {total_tre / success_count:.3f} px\n")
                
        return filepath
