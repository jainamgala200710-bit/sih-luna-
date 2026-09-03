# Reproducibility Verification

For the ISRO Evaluation Committee: We guarantee that all mathematical benchmarks and geometric outcomes generated during our physical demonstration are 100% reproducible on any external machine.

To mathematically audit our claims, execute the automated testing architecture.

## 1. Environment Standardization
```bash
git clone https://github.com/dhamalavishkar/sih26166.git
cd sih26166
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Execute the Edge-Case Exhaustion Suite
This validates our claims that classical SIFT physically shatters at 20x scale drops and extreme illumination inversions, proving the necessity of our Phase 12 LoFTR integration.
```bash
py -m pytest tests/edge_cases/
```
**Expected Output**: `3 passed` (Proving that the `PipelineExhaustionError` successfully intercepts the theoretical boundaries).

## 3. Execute the Full Backend Integration Pipeline
This validates the sub-pixel calculations and the autonomous HTML Report Generator.
```bash
py -m pytest tests/integration/test_full_pipeline.py
```
**Expected Output**: `1 passed`. The pipeline will autonomously calculate the affine matrix and dump the resulting base64 encoded HTML report into your local `backend/cache/results/` directory, exactly as demonstrated on stage.
