import os
import csv
import random
from typing import List, Dict, Tuple

class TrainTestSplitter:
    """
    Splits the pair inventory into Train, Validation, and Test sets.
    """
    def __init__(self, splits_dir: str = "data/splits"):
        self.splits_dir = splits_dir
        os.makedirs(self.splits_dir, exist_ok=True)

    def split(self, inventory_path: str, ratios: Tuple[float, float, float] = (0.7, 0.15, 0.15), seed: int = 42):
        """
        Splits pairs randomly into train/val/test and saves CSV files for each.
        """
        assert sum(ratios) == 1.0, "Ratios must sum to 1.0"
        
        if not os.path.exists(inventory_path):
            raise FileNotFoundError(f"Inventory not found: {inventory_path}")
            
        pairs = []
        fieldnames = []
        with open(inventory_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            pairs = list(reader)
            
        random.seed(seed)
        random.shuffle(pairs)
        
        n = len(pairs)
        train_end = int(n * ratios[0])
        val_end = train_end + int(n * ratios[1])
        
        splits = {
            "train": pairs[:train_end],
            "val": pairs[train_end:val_end],
            "test": pairs[val_end:]
        }
        
        for split_name, split_data in splits.items():
            split_file = os.path.join(self.splits_dir, f"{split_name}_pairs.csv")
            with open(split_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(split_data)
                
        return {k: len(v) for k, v in splits.items()}
