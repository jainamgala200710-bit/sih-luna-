# Frontend-Backend Integration Architecture (Phase 22)

## Overview
Phase 22 seamlessly fuses the Vite + React client dashboard with the asynchronous FastAPI mathematical backend. By leveraging dual protocols (HTTP + WebSockets), the application maintains extreme responsiveness while executing deeply intensive CPU pipelines (OpenCV / SIFT / Matrix solvers) in the background.

## Sequence of Events

1. **Ingestion (HTTP POST)**: 
   - The user drops dual images into the `UploadPanel` component. 
   - The `apiService.uploadImages` wrapper executes a `multipart/form-data` payload to `POST /api/v1/upload`.
   - The backend allocates a localized `session_id` cache and returns it.

2. **Trigger (HTTP POST & WebSocket)**:
   - The React client connects a native browser `WebSocket` to `ws://localhost:8000/ws/progress/{session_id}`.
   - Simultaneously, the client issues `POST /api/v1/registration/{session_id}`.
   - FastAPI spins up a `BackgroundTasks` thread to run `RegistrationService.execute_pipeline` without blocking the HTTP response.

3. **Telemetry Streaming**:
   - As the OpenCV pipeline crunches matrices, it hits `await manager.broadcast_progress` injection hooks.
   - The WebSocket pumps JSON payloads (e.g., `{"stage": "verified", "progress": 60}`) back to React.
   - The `App.jsx` `useEffect` hook intercepts these payloads and updates the `PipelineVisualizer` UI in real-time.

4. **Result Resolution (HTTP GET)**:
   - Once the backend transmits `stage: "complete"`, the WebSocket terminates.
   - React dynamically auto-switches to the `MatchVisualizer` view.
   - The component executes `apiService.fetchResults` triggering a `GET` against `/results/{session_id}/summary` and subsequently pulling the Explainability Dossiers (JSON + PNG) directly into the view.
