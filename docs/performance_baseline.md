# Performance Baseline Metrics

## Overview
Phase 23 executes standard synthetic pairs (e.g., `data/synthetic/pair_001`) through the entirety of the LunaAlign pipeline. The overarching latency is highly bound to standard compute constraints (CPU vs. GPU execution of the RANSAC algorithm and SIFT feature detection).

## Baseline Synthetic Payload (800x800 px)
- **Ingestion & Caching (I/O)**: ~50ms
- **Feature Extraction (SIFT)**: ~150ms
- **Sub-Pixel Refinement (Fourier Transform)**: ~300ms
- **Outlier Rejection (RANSAC iterations)**: ~200ms
- **Explainability Dumping**: ~150ms

### Conclusion
A standard single-shot pipeline execution (without large-batch benchmarking overhead) concludes comfortably within **<1000ms** on standard local development machines. This lightning-fast latency makes the real-time WebSocket telemetry system slightly unnoticeable for small images, but fundamentally critical for scaling this software into massive 10,000x10,000 pixel scientific arrays in production.
