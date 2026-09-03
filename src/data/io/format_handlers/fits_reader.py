import numpy as np
from typing import Tuple, Dict

def read_fits(file_path: str) -> Tuple[np.ndarray, Dict]:
    """
    Reads a FITS image and extracts basic metadata.
    Requires 'astropy' library.
    """
    try:
        from astropy.io import fits
    except ImportError:
        raise ImportError(
            "The 'astropy' library is required to read FITS files. "
            "Please install it using: py -m pip install astropy"
        )
        
    with fits.open(file_path) as hdul:
        # Get the first image extension
        image_data = None
        header = None
        for hdu in hdul:
            if isinstance(hdu, (fits.PrimaryHDU, fits.ImageHDU)) and hdu.data is not None:
                image_data = hdu.data
                header = hdu.header
                break
                
        if image_data is None:
            raise ValueError(f"No image data found in FITS file: {file_path}")
            
        metadata = dict(header) if header else {}
        
        # Convert to float32 numpy array for consistent processing
        return image_data.astype(np.float32), metadata
