import subprocess
import time
import os
import sys

def check_dependencies():
    print("Checking dependencies...")
    try:
        subprocess.run(["py", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True, shell=True)
    except Exception as e:
        print("ERROR: Python or NPM is not installed/accessible in PATH.")
        sys.exit(1)

def boot_servers():
    print("\n--- Booting LunaAlign Architecture ---")
    
    # Start Backend API
    print("Booting FastAPI Backend (Port 8000)...")
    backend_proc = subprocess.Popen(["py", "-m", "uvicorn", "backend.main:app"], cwd=os.getcwd())
    
    # Wait a sec for backend to bind port
    time.sleep(3)
    
    # Start Frontend UI
    print("Booting React Frontend (Port 5173)...")
    frontend_proc = subprocess.Popen(["npm", "run", "dev"], cwd=os.path.join(os.getcwd(), "frontend"), shell=True)
    
    print("\n--- SYSTEM ONLINE ---")
    print("API: http://localhost:8000")
    print("UI:  http://localhost:5173")
    print("Pre-loaded Demo Sets available in: demo/chandrayaan2_lroc_pairs/")
    print("\nPress Ctrl+C to shutdown.")
    
    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down LunaAlign...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    check_dependencies()
    boot_servers()
