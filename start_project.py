import os
import sys
import subprocess
import threading
import time
import requests
import webbrowser
from pathlib import Path

# Dynamically detect the current Python executable
PYTHON_EXEC = Path(sys.executable)

# Define project directory paths
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / 'backend'
FRONTEND_DIR = BASE_DIR / 'frontend'

# URLs
API_URL = 'http://127.0.0.1:5000/data'
FRONTEND_URL = 'http://127.0.0.1:8000/'

def start_backend():
    """Start the backend Flask server."""
    if not BACKEND_DIR.exists():
        print(f"❌ Backend directory not found at {BACKEND_DIR}")
        return

    print(f"🚀 Starting backend from: {BACKEND_DIR}")
    process = subprocess.Popen(
        [str(PYTHON_EXEC), 'app.py'],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ
    )

    def log_output():
        for line in process.stdout:
            print("🔧 [Backend]", line.decode().rstrip())

    threading.Thread(target=log_output, daemon=True).start()
    return process

def start_frontend():
    """Start the frontend using a simple HTTP server."""
    if not FRONTEND_DIR.exists():
        print(f"❌ Frontend directory not found at {FRONTEND_DIR}")
        return

    print(f"🌐 Starting frontend server from: {FRONTEND_DIR}")
    subprocess.Popen(
        [str(PYTHON_EXEC), '-m', 'http.server', '8000'],
        cwd=FRONTEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def check_backend_health():
    """Check if the backend API is responding."""
    print("⏳ Waiting for backend to be ready...")
    for _ in range(10):
        try:
            response = requests.get(API_URL, timeout=3)
            if response.status_code == 200:
                print("✅ Backend is running.")
                return True
        except requests.RequestException:
            time.sleep(1.5)
    print("❌ Backend failed to start.")
    return False

def open_browser():
    """Open the frontend in the default web browser."""
    print("🌍 Opening dashboard in browser...")
    webbrowser.open(FRONTEND_URL)

if __name__ == "__main__":
    print("📦 Initializing MoMo Data Analysis Project")
    print(f"📂 Project root: {BASE_DIR}")
    print(f"🐍 Python used: {PYTHON_EXEC}")

    backend_proc = start_backend()

    if check_backend_health():
        start_frontend()
        time.sleep(1)
        open_browser()
    else:
        print("🚫 Project failed to launch. Check backend configuration.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down by user. Goodbye!")
