# Visualization Dashboard Setup

## Overview
The Phase 20 `frontend` serves as the primary visual telemetry interface for the LunaAlign AI registration system. Rather than relying solely on programmatic JSON dumps or terminal logs, scientific users will access this localized Vite + React application to inspect algorithmic behavior, view matching geometries, and overlay warped projections to physically confirm alignment accuracy.

## Architecture
- **Framework**: React via Vite (Lightning fast HMR).
- **Styling**: Native CSS (`index.css`) designed exclusively for premium dark mode telemetry without external atomic CSS libraries (e.g., Tailwind) allowing complete modular design control.
- **Icons**: `lucide-react`.

## Directory Structure
- `src/components/ImageViewer.jsx`: Dual-pane ingestion visualization.
- `src/components/MatchVisualizer.jsx`: Correspondence graph rendering surface.
- `src/components/ComparisonModes.jsx`: Alpha blending and slider swipe tools for registered validation.
- `src/components/PipelineVisualizer.jsx`: Pipeline state telemetry mapping node completion.

## How to Run
```bash
cd frontend
npm install
npm run dev
```

The application will bind to a local node server (`http://localhost:5173/`). Currently, the layout operates with static mock data. API integrations linking the Python OpenCV backend to this React frontend are defined in Phase 21.
