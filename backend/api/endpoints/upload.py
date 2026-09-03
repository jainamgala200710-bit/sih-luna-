from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
import shutil

router = APIRouter()

@router.post("/")
async def upload_image_pair(source: UploadFile = File(...), reference: UploadFile = File(...)):
    """
    Ingests binary image payloads from the dashboard, allocating them a unique Session ID 
    so concurrent scientists can run overlapping experiments.
    """
    if not source.filename or not reference.filename:
        raise HTTPException(status_code=400, detail="Both source and reference files are required")
        
    session_id = str(uuid.uuid4())
    session_dir = f"backend/cache/images/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    
    src_path = os.path.join(session_dir, "source.png")
    ref_path = os.path.join(session_dir, "reference.png")
    
    try:
        with open(src_path, "wb") as f_src:
            shutil.copyfileobj(source.file, f_src)
            
        with open(ref_path, "wb") as f_ref:
            shutil.copyfileobj(reference.file, f_ref)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cache files: {str(e)}")
    finally:
        source.file.close()
        reference.file.close()
        
    return {
        "session_id": session_id,
        "message": "Images successfully cached and ready for registration."
    }
