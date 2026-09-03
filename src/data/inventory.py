import os
import csv
from typing import Dict, List, Optional
from datetime import datetime

class DataInventory:
    """
    Manages the data inventory for Lunar images.
    """
    def __init__(self, inventory_file: str = "data/inventory.csv"):
        self.inventory_file = inventory_file
        self.fieldnames = [
            "image_id", "mission", "instrument", "acquisition_date", 
            "spatial_resolution", "file_path", "file_format", "processing_level"
        ]
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates the inventory file and header if it doesn't exist."""
        os.makedirs(os.path.dirname(os.path.abspath(self.inventory_file)), exist_ok=True)
        if not os.path.exists(self.inventory_file):
            with open(self.inventory_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def add_image(self, metadata: Dict) -> bool:
        """Adds a new image record to the inventory."""
        # Basic validation
        for field in self.fieldnames:
            if field not in metadata and field != "acquisition_date":
                # Only enforce some required fields loosely for now
                pass
        
        # Check if already exists
        if self.get_image(metadata.get("image_id")):
            return False
            
        with open(self.inventory_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            # Filter metadata to only include known fieldnames
            row = {k: v for k, v in metadata.items() if k in self.fieldnames}
            writer.writerow(row)
        return True

    def get_image(self, image_id: str) -> Optional[Dict]:
        """Retrieves an image record by its ID."""
        if not os.path.exists(self.inventory_file):
            return None
            
        with open(self.inventory_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("image_id") == image_id:
                    return row
        return None

    def list_images(self) -> List[Dict]:
        """Returns all image records."""
        if not os.path.exists(self.inventory_file):
            return []
            
        with open(self.inventory_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

if __name__ == "__main__":
    # Simple test
    inventory = DataInventory()
    print("Inventory initialized at:", inventory.inventory_file)
