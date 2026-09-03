# Quick Start Guide for ISRO Evaluators

Welcome to the LunaAlign Analytical Engine. To boot the full-stack architecture locally on your machine, follow these three commands.

## Requirements
- Python 3.9+
- Node.js & NPM

## Installation

1. **Clone and Install Dependencies**
```bash
# Python Backend Requirements
pip install -r requirements.txt

# React Frontend Requirements
cd frontend
npm install
cd ..
```

2. **Boot the System**
We have provided a unified boot script that securely binds the FastAPI server and the Vite React server across local ports.
```bash
python demo/demo_script.py
```

3. **Operate**
- Open `http://localhost:5173` in your browser.
- Open the `demo/chandrayaan2_lroc_pairs/ideal` folder on your desktop.
- Drag and drop `source.png` and `reference.png` into the respective Upload zones.
- Click **"Run Coregistration"**.

*The output mathematical report will be dynamically deposited as a standalone HTML file inside `backend/cache/results/`.*
