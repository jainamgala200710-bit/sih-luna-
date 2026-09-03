import os

def detect_format(file_path: str) -> str:
    """
    Detects the scientific or standard image format based on file extension and header.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.fits', '.fit']:
        return 'FITS'
    elif ext in ['.lbl', '.xml']:
        # Often PDS labels
        return 'PDS'
    elif ext == '.img':
        # Could be PDS or ISRO IMG. We will classify as 'IMG' and let the handler decide.
        return 'IMG'
    elif ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff']:
        return 'STANDARD'
    else:
        return 'UNKNOWN'
