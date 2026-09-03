import pytest
from fastapi.testclient import TestClient
import os
import shutil

from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_upload_endpoint():
    """
    Validates that the upload endpoint properly parses multipart/form-data
    and caches the binary files under a generated UUID directory.
    """
    src_path = "data/synthetic/pair_001/source.png"
    ref_path = "data/synthetic/pair_001/reference.png"
    
    with open(src_path, "rb") as f_src, open(ref_path, "rb") as f_ref:
        response = client.post(
            "/api/v1/upload/",
            files={"source": ("source.png", f_src, "image/png"), 
                   "reference": ("reference.png", f_ref, "image/png")}
        )
        
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    
    session_id = data["session_id"]
    
    # Verify files created on disk
    assert os.path.exists(f"backend/cache/images/{session_id}/source.png")
    assert os.path.exists(f"backend/cache/images/{session_id}/reference.png")
    
    # Cleanup
    shutil.rmtree(f"backend/cache/images/{session_id}", ignore_errors=True)

def test_registration_trigger_endpoint():
    """
    Validates that hitting the execution trigger immediately returns a 200 
    without blocking, as the background task is queued.
    """
    dummy_session = "api_test_session"
    response = client.post(f"/api/v1/registration/{dummy_session}")
    assert response.status_code == 200
    assert response.json()["message"] == "Registration pipeline queued"
