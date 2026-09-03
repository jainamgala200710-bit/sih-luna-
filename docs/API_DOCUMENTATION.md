# LunaAlign API Documentation

## Overview
The Phase 21 Python Backend is built on **FastAPI** to provide extreme asynchronous throughput connecting the Frontend React Dashboard to the mathematical computer vision core. 

## Endpoints

### 1. Ingestion Layer
`POST /api/v1/upload/`
- **Payload**: `multipart/form-data` with `source` and `reference` binaries.
- **Action**: Caches the imagery on the server block.
- **Returns**: `session_id`

### 2. Execution Layer
`POST /api/v1/registration/{session_id}`
- **Payload**: None.
- **Action**: Injects the Session ID into the background Task Executor. The mathematical pipeline will execute asynchronously without blocking the HTTP thread.
- **Returns**: Acknowledgment.

`WS /ws/progress/{session_id}`
- **Protocol**: WebSocket.
- **Action**: The frontend connects to this socket. The `RegistrationService` broadcasts state transitions (`raw`, `matched`, `verified`, `registered`) and percentile progress metrics during the 10-20s execution window.

### 3. Telemetry Layer
`GET /api/v1/results/{session_id}/summary`
- **Returns**: Core JSON containing RMSE, Inlier counts, and Transformation models.

`GET /api/v1/results/{session_id}/dossier/{idx}`
- **Returns**: The generated JSON explainability metrics for a specific target match.

`GET /api/v1/results/{session_id}/dossier/{idx}/image/{type}`
- **Returns**: Binary image payloads for rendering in the dashboard. Valid types: `patch`, `src_uncertainty`, `ref_uncertainty`.
