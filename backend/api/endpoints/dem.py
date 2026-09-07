from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import json
import logging
from backend.services.dem_service import DemService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/{session_id}/generate")
async def generate_dem_model(session_id: str):
    """
    Computes 3D Digital Elevation Model (DEM) from the stereo pair using OpenCV StereoSGBM.
    """
    try:
        data = DemService.generate_dem(session_id)
        return {"status": "success", "data": data}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error computing DEM: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"DEM computation failed: {str(e)}")

@router.get("/{session_id}/data")
async def get_dem_data(session_id: str):
    """
    Returns the JSON 3D height grid and elevation telemetry for Three.js rendering.
    """
    json_path = f"backend/cache/results/{session_id}/dem_data.json"
    if not os.path.exists(json_path):
        # Compute on demand if not already generated
        try:
            return DemService.generate_dem(session_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"DEM data not found: {str(e)}")
            
    with open(json_path, "r") as f:
        return json.load(f)

@router.get("/{session_id}/image/{img_type}")
async def get_dem_image(session_id: str, img_type: str):
    """
    Returns visual DEM elevation maps: 'colormap' or 'disparity'.
    """
    mapping = {
        'colormap': 'dem_colormap.png',
        'disparity': 'dem_disparity.png'
    }
    
    if img_type not in mapping:
        raise HTTPException(status_code=400, detail="Invalid DEM image type. Use 'colormap' or 'disparity'.")
        
    img_path = f"backend/cache/results/{session_id}/{mapping[img_type]}"
    if not os.path.exists(img_path):
        # Attempt generation if images exist
        try:
            DemService.generate_dem(session_id)
        except Exception:
            raise HTTPException(status_code=404, detail="DEM image not found or not yet generated.")
            
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="DEM image not found.")
        
    return FileResponse(img_path)
