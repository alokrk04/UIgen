import this

this #!/usr/bin/env python3
"""
🚀 SIMPLE FULL-STACK RUNNER - WORKING VERSION
Just run backend and frontend, no complicated environment setup
"""

import subprocess
import os
import sys
import time
import signal
import atexit

PROJECT_DIR = "/Users/alok/Desktop/Customer churn Predictor"
NODE_DIR = os.path.expanduser("~/.local/opt/node")
BACKEND_LOG = "/tmp/backend.log"
FRONTEND_LOG = "/tmp/frontend.log"

os.chdir(PROJECT_DIR)

processes = []

def cleanup():
    print("\n\n🛑 Shutting down...")
    for p in processes:
        try:
            if p.poll() is None:
                p.terminate()
                time.sleep(1)
                if p.poll() is None:
                    p.kill()
        except:
            pass
    print("✅ Done")

atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

print("╔══════════════════════════════════════════════════════════════════╗")
print("║  🚀 CHURN PREDICTION SYSTEM - FULL STACK                         ║")
print("║  Starting Backend + Frontend                                     ║")
print("╚══════════════════════════════════════════════════════════════════╝\n")

# Kill any existing processes
print("🧹 Cleaning up old processes...")
os.system("pkill -f 'uvicorn backend' 2>/dev/null || true")
os.system("pkill -f 'next dev' 2>/dev/null || true")
time.sleep(1)

# Install dependencies
print("\n📦 Installing Python dependencies...")
result = subprocess.run(
    f"{sys.executable} -m pip install -q -r backend/requirements.txt",
    shell=True,
    capture_output=True
)
print("✅ Python dependencies ready")

# Start backend
print("\n🔧 Starting Backend (FastAPI on port 8000)...")
with open(BACKEND_LOG, 'w') as log_file:
    backend_proc = subprocess.Popen(
        f"{sys.executable} -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload",
        shell=True,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=PROJECT_DIR
    )
    processes.append(backend_proc)
    print(f"✅ Backend started (PID: {backend_proc.pid})")
    print(f"   Logs: {BACKEND_LOG}")

time.sleep(3)

# Start frontend
print("\n🌐 Starting Frontend (Next.js on port 3000)...")
print("   This may take 30-60 seconds to compile...")

env = os.environ.copy()
env['PATH'] = f"{NODE_DIR}/bin:{env.get('PATH', '')}"

frontend_cmd = f"{NODE_DIR}/bin/node {NODE_DIR}/lib/node_modules/npm/bin/npm-cli.js run dev"

with open(FRONTEND_LOG, 'w') as log_file:
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        shell=True,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=f"{PROJECT_DIR}/frontend",
        env=env
    )
    processes.append(frontend_proc)
    print(f"✅ Frontend started (PID: {frontend_proc.pid})")
    print(f"   Logs: {FRONTEND_LOG}")

time.sleep(3)

# Success message
print("\n" + "╔" + "="*68 + "╗")
print("║" + " "*68 + "║")
print("║" + " "*10 + "✅ SUCCESS! BOTH SERVERS NOW RUNNING! ✅" + " "*18 + "║")
print("║" + " "*68 + "║")
print("╠" + "="*68 + "╣")
print("║" + " "*68 + "║")
print("║  📱 FRONTEND:    http://localhost:3000" + " "*26 + "║")
print("║  🔌 BACKEND:     http://localhost:8000" + " "*25 + "║")
print("║  📚 API DOCS:    http://localhost:8000/docs" + " "*19 + "║")
print("║" + " "*68 + "║")
print("║  Test Datasets:" + " "*52 + "║")
print("║    • data/telecom_churn_data.csv" + " "*33 + "║")
print("║    • CSV's/BankChurners.csv" + " "*38 + "║")
print("║    • CSV's/patient_churn_dataset.csv" + " "*29 + "║")
print("║" + " "*68 + "║")
print("║  ⌨️  Press Ctrl+C to stop all servers" + " "*28 + "║")
print("║" + " "*68 + "║")
print("╚" + "="*68 + "╝\n")

# Monitor
print("✅ Monitoring processes... (Ctrl+C to stop)\n")
try:
    while True:
        time.sleep(1)
        if backend_proc.poll() is not None:
            print("❌ Backend died!")
            break
        if frontend_proc.poll() is not None:
            print("❌ Frontend exited!")
            break
except KeyboardInterrupt:
    print("\n\n⏸️ Interrupted")

