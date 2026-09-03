import os
import cv2
import numpy as np
from typing import Tuple, Dict

from src.data.io.format_detection import detect_format

class DataLoader:
    """
    Main interface for ingesting scientific and standard images.
    Automatically routes to the appropriate format handler based on file type.
    """
    def __init__(self):
        pass
        
    def load_image(self, file_path: str) -> Tuple[np.ndarray, Dict]:
        """
        Loads an image from the given path, returning the image array and metadata.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
            
        fmt = detect_format(file_path)
        
        if fmt == 'FITS':
            from src.data.io.format_handlers.fits_reader import read_fits
            return read_fits(file_path)
            
        elif fmt == 'PDS':
            from src.data.io.format_handlers.pds_reader import read_pds
            return read_pds(file_path)
            
        elif fmt == 'IMG':
            from src.data.io.format_handlers.img_reader import read_img
            return read_img(file_path)
            
        elif fmt == 'STANDARD':
            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            if img is None:
                raise ValueError(f"OpenCV failed to read standard image: {file_path}")
            metadata = {
                "format": "STANDARD",
                "dimensions": img.shape,
                "dtype": str(img.dtype)
            }
            return img.astype(np.float32), metadata
            
        else:
            raise ValueError(f"Unsupported or unknown file format for file: {file_path}")

if __name__ == "__main__":
    # Simple test for standard image
    loader = DataLoader()
    print("DataLoader successfully instantiated.")
