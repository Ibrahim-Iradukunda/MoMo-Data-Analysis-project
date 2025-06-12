import os
import subprocess
import threading
import time
import requests
import webbrowser

# Find the path to python3 (default to /usr/bin/python3)
PYTHON3_PATH = os.popen('which python3').read().strip() or '/usr/bin/python3'

def start_backend():
    # Change to backend directory from project root
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    print(f"Attempting to change to backend directory: {backend_dir}")
    if not os.path.exists(backend_dir):
        print(f"Error: Backend directory not found at {backend_dir}")
        return
    os.chdir(backend_dir)
    print(f"Starting backend from: {os.getcwd()}")
    # Use full path to python3 and inherit environment
    subprocess.Popen([PYTHON3_PATH, 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)

def start_frontend():
    # Change to frontend directory from project root
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    print(f"Attempting to change to frontend directory: {frontend_dir}")
    if not os.path.exists(frontend_dir):
        print(f"Error: Frontend directory not found at {frontend_dir}")
        return
    os.chdir(frontend_dir)
    print(f"Starting frontend from: {os.getcwd()}")
    # Use full path to python3 and inherit environment
    os.system(f'{PYTHON3_PATH} -m http.server 8000')

def check_backend_health():
    # Wait for backend to be ready (check /data endpoint)
    max_attempts = 10
    for _ in range(max_attempts):
        try:
            response = requests.get('http://127.0.0.1:5000/data', timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            time.sleep(2)  # Wait 2 seconds before retrying
    return False

def open_browser():
    # Open browser after backend and frontend are ready
    webbrowser.open('http://0.0.0.0:8000/')

if __name__ == "__main__":
    print(f"Script location: {os.path.dirname(__file__)}")
    print(f"Using Python3 path: {PYTHON3_PATH}")
    # Start backend in a separate process
    backend_process = threading.Thread(target=start_backend)
    backend_process.daemon = True
    backend_process.start()

    # Wait for backend to be ready
    print("Waiting for backend to start...")
    if check_backend_health():
        print("Backend is ready. Starting frontend...")
        
        # Start frontend in a separate thread
        frontend_thread = threading.Thread(target=start_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()

        # Wait a second for frontend to start
        time.sleep(1)
        open_browser()
    else:
        print("Failed to start backend. Please check the backend logs.")

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Project stopped by user.")