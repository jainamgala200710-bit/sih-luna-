import os
import base64
from string import Template
from datetime import datetime

class ReportGenerator:
    """
    Asynchronously parses the cache directories upon pipeline completion,
    compiles the physical matrices, converts raw image binaries to base64,
    and generates a standalone Scientific HTML Report.
    """
    
    @staticmethod
    def _image_to_base64(filepath: str) -> str:
        if not os.path.exists(filepath):
            return ""
        with open(filepath, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
            
    @staticmethod
    def _format_matrix(matrix: list) -> str:
        if not matrix:
            return "N/A"
        formatted = ""
        for row in matrix:
            formatted += "[ " + "  ".join([f"{val:12.6f}" for val in row]) + " ]\n"
        return formatted

    @staticmethod
    def generate(session_id: str, results: dict, cache_dir: str = "backend/cache") -> str:
        # Load Template
        template_path = "src/reporting/report_template.html"
        with open(template_path, 'r') as f:
            template_str = f.read()
            
        template = Template(template_str)
        
        # Paths
        src_path = os.path.join(cache_dir, f"images/{session_id}/source.png")
        ref_path = os.path.join(cache_dir, f"images/{session_id}/reference.png")
        # Find the dossier visualization if it exists
        dossier_idx = results.get("dossier_index", -1)
        matches_path = os.path.join(cache_dir, f"results/{session_id}/dossiers/dossier_{dossier_idx}/local_patch_matches.png")
        if not os.path.exists(matches_path):
            # Fallback if specific dossier missing
            matches_path = os.path.join(cache_dir, f"images/{session_id}/source.png") # Just fallback for now
            
        # Encode Images
        src_b64 = ReportGenerator._image_to_base64(src_path)
        ref_b64 = ReportGenerator._image_to_base64(ref_path)
        match_b64 = ReportGenerator._image_to_base64(matches_path)
        
        status = "SUCCESS" if results.get("rmse") != "FAILED" else "FAILED"
        status_color = "#2e7d32" if status == "SUCCESS" else "#c62828"
        
        # Map values
        mapping = {
            "session_id": session_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "model_name": results.get("model", "N/A").upper(),
            "rmse": results.get("rmse", "N/A"),
            "inliers": results.get("inliers", 0),
            "total_matches": results.get("total_matches", 0),
            "status": status,
            "status_color": status_color,
            "h_matrix": ReportGenerator._format_matrix(results.get("H_matrix", [])),
            "source_b64": src_b64,
            "reference_b64": ref_b64,
            "matches_b64": match_b64
        }
        
        html_content = template.safe_substitute(mapping)
        
        # Save output
        output_path = os.path.join(cache_dir, f"results/{session_id}/ISRO_LunaAlign_Report.html")
        with open(output_path, "w") as f:
            f.write(html_content)
            
        return output_path
