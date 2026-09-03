# Getting Started

## 1. Environment Initialization
LunaAlign requires an isolated Python environment to prevent dependency collisions with host GIS software (like QGIS or ArcGIS).

```bash
# Verify Python
py --version # Must be 3.9+

# Install Backend
pip install -r requirements.txt

# Install Frontend
cd frontend
npm install
```

## 2. Booting the Engine
For operators, we have decoupled the complex microservices into a single `demo_script.py` bootloader.

```bash
py demo/demo_script.py
```
This single command spins up:
1. `uvicorn` FastAPI REST Endpoint & WebSocket telemetry stream (Port 8000).
2. `vite` React Interface (Port 5173).

## 3. Performing Registration
1. Navigate to `http://localhost:5173`.
2. Provide a **Source** (Unregistered payload) and a **Reference** (Geo-locked base map).
3. The UI will autonomously track the mathematical progress across:
   - SIFT Feature Extraction
   - Sub-Pixel Phase-Correlation
   - RANSAC Outlier Rejection
   - Homography Model Selection
4. Upon completion, a physical HTML Scientific Report will be deposited into `backend/cache/results/`.
