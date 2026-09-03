# Troubleshooting Guide

## Environment Issues

### 1. `ModuleNotFoundError: No module named 'cv2'`
**Cause**: The Python environment is missing the OpenCV C++ bindings.
**Fix**: Ensure you have installed the core requirements.
```bash
pip install -r requirements.txt
```

### 2. `uvicorn is not recognized as an internal or external command`
**Cause**: Uvicorn is installed globally but not in your system PATH, or you are outside of your virtual environment.
**Fix**: Prepend `py -m` to the execution to force Python to route the module.
```bash
py -m uvicorn backend.main:app
```
*(Note: Our `demo_script.py` automatically implements this fix).*

## Execution Issues

### 3. PipelineExhaustionError (Red UI Flash)
**Cause**: The orbital imagery you uploaded has a scale variance greater than 4x or a physical illumination gradient that SIFT mathematically cannot process.
**Fix**: Click the **"Algorithm Engine"** toggle in the React UI and switch to the **LoFTR Deep Learning Engine**.

### 4. Out of Memory (OOM) / Process Killed
**Cause**: You attempted to upload a multi-gigabyte TIFF directly into the classical engine, bypassing the chunker.
**Fix**: Ensure `TilingEngine` is set to `True` in the backend parameters, which will forcefully grid-slice the image into `1000x1000` arrays.
