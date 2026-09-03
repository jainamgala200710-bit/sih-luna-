# Supported Formats: LunaAlign AI

LunaAlign AI is designed to handle a variety of scientific image formats common in planetary missions, alongside standard image formats.

## 1. Standard Formats
- **PNG / JPEG**: Common formats used for synthetic datasets and quick previews. Handled natively via OpenCV.
- **TIFF**: Supported for georeferenced or high-depth images. Handled via OpenCV / Scipy.

## 2. Scientific Formats (Requires specific libraries)
- **FITS (Flexible Image Transport System)**: Standard astronomical format. 
  - *Extension*: `.fits`, `.fit`
  - *Handler*: `fits_reader.py` (Requires `astropy`)
- **PDS3 / PDS4 (Planetary Data System)**: NASA standard for planetary data (LRO NAC).
  - *Extension*: `.img`, `.lbl`, `.xml`
  - *Handler*: `pds_reader.py` (Requires `pds4_tools` or `pvl`)
- **ISRO IMG**: Specific format used in Chandrayaan-2 datasets (often similar to PDS or FITS, or standard RAW).
  - *Extension*: `.img`
  - *Handler*: `img_reader.py`

## Implementation Details
The `data_loader.py` acts as a facade. It automatically detects the file format using `format_detection.py` and delegates the parsing to the appropriate handler in `format_handlers/`.

If a specialized library (like `astropy`) is not installed, the loader will gracefully raise an `ImportError` detailing how to install the required dependency.
