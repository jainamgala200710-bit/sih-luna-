# LunaAlign System Architecture

## Overview
LunaAlign is a full-stack, cross-modal image registration application engineered specifically for aligning multi-sensor scientific imagery (e.g., optical vs. SAR). The system architecture decouples the intensive OpenCV mathematical execution from the interactive Web interface via an asynchronous Python middle-layer.

## Layer 1: Presentation Layer (Vite + React)
- **Role**: Provides the interactive Dashboard.
- **Components**:
  - `UploadPanel`: Ingests raw binary imagery via HTML5 drag-and-drop.
  - `PipelineVisualizer`: Native CSS rendering of the execution state.
  - `ResultsViewer`: Renders Explainability JSONs and visualizes matched topologies.
- **Network Protocol**: Standard HTTP `fetch` for binary uploads and REST pulls, augmented with `WebSocket` connections for active telemetry.

## Layer 2: API Gateway (FastAPI)
- **Role**: Acts as the asynchronous broker, ensuring the main HTTP thread never blocks.
- **Execution Model**: Utilizes `BackgroundTasks` to offload the mathematical pipeline into separate execution threads.
- **State Management**: The `ConnectionManager` hashes specific WebSocket strings to local `session_id` UUIDs, ensuring that multiple concurrent scientific sessions don't bleed telemetry.

## Layer 3: The Mathematical Pipeline (OpenCV + Python)
- **Role**: The core Engine.
- **Topology**:
  1. `ClassicalMatchingPipeline`: Ingests arrays, extracts multi-octave features (SIFT/ORB), and matches them via KNN algorithms.
  2. `SubPixelRefinementPipeline`: Enforces sub-pixel accuracy by cropping local windows and applying Fourier-space Phase Correlation.
  3. `ModelValidationPipeline`: Iterates through Affine, Partial-Affine, and Homographic hypotheses using RANSAC to calculate the definitive transformation matrix.
  4. `ExplainabilityPipeline`: Reverse-engineers the chosen topology, printing human-readable JSON dossiers quantifying *why* the matrix warped correctly.
