# SIH26166 Demonstration Script: LunaAlign

## 0:00 - 1:00: Problem Statement & Boot
**Action**: Open terminal and execute `py demo/demo_script.py`. 
**Talking Point**: "Good morning judges. We are solving SIH26166: Coregistration of multi-modal lunar imagery like Chandrayaan-2 TMC and LRO/OHRC. As you can see, our full-stack architecture boots autonomously with a single command."
**Action**: Open `http://localhost:5173` in the browser.

## 1:00 - 2:30: The "Ideal" Baseline
**Action**: Drag and drop `demo/chandrayaan2_lroc_pairs/ideal/source.png` and `reference.png` into the React UI. Click "Run Coregistration".
**Talking Point**: "First, we demonstrate standard temporal alignment. The React frontend streams the binaries to our FastAPI backend via REST, while WebSockets pipe real-time extraction telemetry back to the vertical status bar."
**Action**: Click into the Results Dashboard.
**Talking Point**: "Our classical SIFT math extracts structural geometries, calculates a rigid affine transformation, and auto-generates a scientific PDF/HTML report. The RMSE here is calculated exactly to the sub-pixel."

## 2:30 - 4:00: The "Extreme Edge-Case" (Cross-Modal)
**Action**: Drag and drop the `extreme/` pairs into the UI. Click "Run Coregistration".
**Talking Point**: "However, the true challenge of SIH26166 is cross-modal math. This is a simulated OHRC vs TMC-2 pair. It has a 20x fractional scale drop, and extreme sun-angle illumination inversion."
**Action**: Wait for the UI to flash the Red Pipeline Exhaustion Error.
**Talking Point**: "Notice what happens. SIFT physically shatters here. But our architecture intercepts the OpenCV memory fault gracefully and warns the operator."
**Action**: Toggle the UI to "Phase 12: Deep Learning (LoFTR)".
**Talking Point**: "We bypass local gradients and route the data through a Kornia LoFTR Semantic probability field. (Explain LoFTR cross-attention)."

## 4:00 - 5:00: Q&A / Scientific Report
**Action**: Open `backend/cache/results/` and click the `ISRO_LunaAlign_Report.html`.
**Talking Point**: "Finally, every successful registration autonomously compiles into a base64-encoded, offline-capable scientific HTML report ready for ISRO publication. We are ready for your questions."
