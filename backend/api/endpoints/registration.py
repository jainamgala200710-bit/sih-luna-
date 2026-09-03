from fastapi import APIRouter, BackgroundTasks, WebSocket, WebSocketDisconnect
from services.registration_service import RegistrationService
from utils.background_tasks import manager

router = APIRouter()

@router.post("/{session_id}")
async def trigger_registration(session_id: str, background_tasks: BackgroundTasks):
    """
    Kicks off the long-running OpenCV pipeline in a FastAPI Background Task
    so the HTTP response returns immediately, preventing timeouts.
    """
    background_tasks.add_task(RegistrationService.execute_pipeline, session_id)
    return {"message": "Registration pipeline queued", "session_id": session_id}

@router.websocket("/ws/progress/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    Establishes the real-time telemetry bridge between the Frontend Dashboard
    and the Background Python Worker.
    """
    try:
        await manager.connect(websocket, session_id)
        try:
            while True:
                # Keep connection alive, wait for client disconnect
                data = await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(session_id)
    except Exception as e:
        print(f"WebSocket error for session {session_id}: {e}")
        # Optionally, you can re-raise or handle the exception
        # But we want to close the connection gracefully
        try:
            await websocket.close()
        except:
            pass