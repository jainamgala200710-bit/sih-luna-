import cv2
import numpy as np
from typing import Tuple, Dict
import os

def read_img(file_path: str) -> Tuple[np.ndarray, Dict]:
    """
    Reads an IMG file. Depending on the source, this might be a raw binary,
    a PDS associated file, or a standard format like ENVI.
    For this generic handler, we attempt to read it via OpenCV, 
    falling back to raw binary interpretation.
    """
    metadata = {"format": "IMG", "source_file": file_path}
    
    # First attempt: standard image parsing via OpenCV
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    
    if img is not None:
        metadata["dimensions"] = img.shape
        metadata["dtype"] = str(img.dtype)
        return img.astype(np.float32), metadata
        
    # Second attempt: Raw binary file without header (requires external knowledge of dimensions)
    # This is common for Chandrayaan-2 raw data.
    raise ValueError(
        f"Cannot automatically parse {file_path}. "
        "IMG files without standard headers require manual dimension and dtype specification."
    )
