import os
import csv
import json
import shutil
from typing import Dict, List, Optional

class PairManager:
    """
    Manages the construction, metadata, and storage of valid image pairs.
    """
    def __init__(self, pairs_inventory: str = "data/pairs/pair_inventory.csv", pairs_dir: str = "data/pairs"):
        self.pairs_inventory = pairs_inventory
        self.pairs_dir = pairs_dir
        self.fieldnames = [
            "pair_id", "source_image_id", "reference_image_id", 
            "pair_type", "overlap_estimate", "pair_quality_score"
        ]
        self._ensure_setup()

    def _ensure_setup(self):
        os.makedirs(self.pairs_dir, exist_ok=True)
        os.makedirs(os.path.join(self.pairs_dir, "synthetic"), exist_ok=True)
        os.makedirs(os.path.join(self.pairs_dir, "real"), exist_ok=True)
        
        os.makedirs(os.path.dirname(os.path.abspath(self.pairs_inventory)), exist_ok=True)
        if not os.path.exists(self.pairs_inventory):
            with open(self.pairs_inventory, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def add_pair(self, metadata: Dict) -> bool:
        """Adds a new pair record to the inventory."""
        for field in self.fieldnames:
            if field not in metadata and field not in ["overlap_estimate", "pair_quality_score"]:
                raise ValueError(f"Missing required field: {field}")
                
        if self.get_pair(metadata.get("pair_id")):
            return False
            
        with open(self.pairs_inventory, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            row = {k: v for k, v in metadata.items() if k in self.fieldnames}
            writer.writerow(row)
        return True

    def get_pair(self, pair_id: str) -> Optional[Dict]:
        if not os.path.exists(self.pairs_inventory):
            return None
        with open(self.pairs_inventory, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("pair_id") == pair_id:
                    return row
        return None

    def construct_pair(self, source_path: str, ref_path: str, pair_id: str, pair_type: str = "synthetic", meta: Dict = None):
        """Constructs a pair directory with images and metadata."""
        if meta is None:
            meta = {}
            
        pair_path = os.path.join(self.pairs_dir, pair_type, pair_id)
        os.makedirs(pair_path, exist_ok=True)
        
        # In a real scenario we'd symlink or copy, we copy here for isolation
        if os.path.exists(source_path):
            shutil.copy(source_path, os.path.join(pair_path, "source.png"))
        if os.path.exists(ref_path):
            shutil.copy(ref_path, os.path.join(pair_path, "reference.png"))
            
        with open(os.path.join(pair_path, "metadata.json"), "w") as f:
            json.dump(meta, f, indent=4)
            
        self.add_pair({
            "pair_id": pair_id,
            "source_image_id": meta.get("source_id", "unknown"),
            "reference_image_id": meta.get("reference_id", "unknown"),
            "pair_type": pair_type,
            "overlap_estimate": meta.get("overlap_estimate", 1.0),
            "pair_quality_score": meta.get("pair_quality_score", 1.0)
        })
        return pair_path
