# SIH Demonstration Backup Plan

If catastrophic environmental failure occurs during live judging (e.g., node modules corruption, python environment collision, or no Wi-Fi), fallback to these pre-rendered mitigations:

## Mitigation 1: Video Walkthrough
Located in the USB Drive given to the judges, `LunaAlign_Full_Walkthrough.mp4` contains a pre-recorded, 3-minute lossless 1080p screen-capture of the entire registration process succeeding.

## Mitigation 2: Pre-Compiled Scientific Reports
If the UI fails to boot, immediately navigate to `backend/cache/results/` and open the pre-compiled `ISRO_LunaAlign_Report.html` files. Because our architecture compiles images directly into the HTML as Base64 strings, these reports can be viewed offline, on any browser, without a server running. 

## Mitigation 3: Fallback to Raw Scripts
If FastAPI or WebSockets collapse, execute the math directly from the command line:
```bash
py tests/integration/test_full_pipeline.py
```
This bypasses the network layer entirely and prints the Homography Matrix and RMSE directly to the terminal stdout.
