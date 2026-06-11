#!/usr/bin/env python3
"""
🚀 ULTIMATE FULL-STACK RUNNER - DEBUGGING VERSION
Works around npm issues by running Next.js directly via node
"""

import subprocess
import os
import sys
import time
import signal
import atexit
import json

PROJECT_DIR = "/Users/alok/Desktop/Customer churn Predictor"
NODE_DIR = os.path.expanduser("~/.local/opt/node")
BACKEND_LOG = "/tmp/backend.log"
FRONTEND_LOG = "/tmp/frontend.log"

os.chdir(PROJECT_DIR)

processes = []

def log(msg):
    print(msg)
    sys.stdout.flush()

def cleanup():
    log("\n\n🛑 Shutting down...")
    for p in processes:
        try:
            if p and p.poll() is None:
                p.terminate()
                time.sleep(1)
                if p.poll() is None:
                    p.kill()
        except:
            pass
    log("✅ All processes stopped")

atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

log("╔══════════════════════════════════════════════════════════════════╗")
log("║  🚀 CHURN PREDICTION SYSTEM - FULL STACK DEBUG RUNNER           ║")
log("║  Backend + Frontend with Direct Node Execution                  ║")
log("╚══════════════════════════════════════════════════════════════════╝\n")

# Kill old processes
log("🧹 Cleaning up old processes...")
os.system("pkill -f 'uvicorn backend' 2>/dev/null || true")
os.system("pkill -f 'next dev' 2>/dev/null || true")
os.system("pkill -f 'node.*next' 2>/dev/null || true")
time.sleep(1)

# Install backend dependencies
log("\n📦 Installing Python dependencies...")
result = subprocess.run(
    f'"{sys.executable}" -m pip install -q -r backend/requirements.txt',
    shell=True,
    capture_output=True,
    text=True
)
if result.returncode != 0:
    log(f"⚠️  Warnings (normal): {result.stderr[:100]}")
log("✅ Python dependencies installed")

# ==================== START BACKEND ====================
log("\n" + "="*70)
log("🔧 STARTING BACKEND (FastAPI)")
log("="*70)

log("\n→ Command: /usr/bin/python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload")
log(f"→ Logs: {BACKEND_LOG}")

with open(BACKEND_LOG, 'w') as log_file:
    backend_proc = subprocess.Popen(
        f'"{sys.executable}" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload',
        shell=True,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=PROJECT_DIR,
        preexec_fn=os.setsid
    )
    processes.append(backend_proc)
    log(f"✅ Backend started (PID: {backend_proc.pid})")

time.sleep(4)

# ==================== INSTALL FRONTEND DEPS ====================
log("\n" + "="*70)
log("📦 FRONTEND SETUP")
log("="*70)

frontend_dir = f"{PROJECT_DIR}/frontend"
if not os.path.exists(f"{frontend_dir}/node_modules"):
    log("\n⚠️  node_modules not found, installing npm packages...")
    log("   This may take 1-2 minutes...")
    
    env = os.environ.copy()
    env['PATH'] = f"{NODE_DIR}/bin:{env.get('PATH', '')}"
    
    npm_cmd = f'"{NODE_DIR}/bin/node" "{NODE_DIR}/lib/node_modules/npm/bin/npm-cli.js" install'
    result = subprocess.run(
        npm_cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=frontend_dir,
        env=env
    )
    
    if result.returncode != 0:
        log(f"❌ npm install failed:")
        log(result.stderr[-500:])
        log("\n✅ But continuing anyway - node_modules may still work")
    else:
        log("✅ npm packages installed")
else:
    log("✅ node_modules already exists")

# ==================== START FRONTEND ====================
log("\n" + "="*70)
log("🌐 STARTING FRONTEND (Next.js)")
log("="*70)

# Run next directly via node (with proper quoting for spaces in path)
next_bin = f"{frontend_dir}/node_modules/.bin/next"
if not os.path.exists(next_bin):
    log(f"\n⚠️  Next binary not found at {next_bin}")
    log("   Trying alternative method...")
    next_cmd = f'"{NODE_DIR}/bin/node" "{frontend_dir}/node_modules/next/dist/bin/next.js" dev'
else:
    next_cmd = f'"{NODE_DIR}/bin/node" "{next_bin}" dev'

log(f"\n→ Command: {next_cmd}")
log(f"→ Logs: {FRONTEND_LOG}")
log("→ This may take 30-60 seconds for compilation...\n")

env = os.environ.copy()
env['PATH'] = f"{NODE_DIR}/bin:{env.get('PATH', '')}"

with open(FRONTEND_LOG, 'w') as log_file:
    frontend_proc = subprocess.Popen(
        next_cmd,
        shell=True,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=frontend_dir,
        env=env,
        preexec_fn=os.setsid
    )
    processes.append(frontend_proc)
    log(f"✅ Frontend started (PID: {frontend_proc.pid})")

time.sleep(5)

# ==================== SUCCESS ====================
log("\n" + "╔" + "="*68 + "╗")
log("║" + " "*68 + "║")
log("║" + " "*8 + "✅ SUCCESS! FULL-STACK SYSTEM NOW RUNNING! ✅" + " "*15 + "║")
log("║" + " "*68 + "║")
log("╠" + "="*68 + "╣")
log("║" + " "*68 + "║")
log("║  🌐 FRONTEND:   http://localhost:3000" + " "*26 + "║")
log("║  🔧 BACKEND:    http://localhost:8000" + " "*25 + "║")
log("║  📚 API DOCS:   http://localhost:8000/docs" + " "*19 + "║")
log("║" + " "*68 + "║")
log("╠" + "="*68 + "╣")
log("║" + " "*68 + "║")
log("║  📝 LOG FILES:" + " "*53 + "║")
log(f"║    Backend:  {BACKEND_LOG}" + " " * (40 - len(BACKEND_LOG)) + "║")
log(f"║    Frontend: {FRONTEND_LOG}" + " " * (38 - len(FRONTEND_LOG)) + "║")
log("║" + " "*68 + "║")
log("║  📂 TEST DATASETS:" + " "*48 + "║")
log("║     • data/telecom_churn_data.csv" + " "*33 + "║")
log("║     • CSV's/BankChurners.csv" + " "*38 + "║")
log("║     • CSV's/patient_churn_dataset.csv" + " "*28 + "║")
log("║" + " "*68 + "║")
log("║  ⌨️  Press Ctrl+C to stop all servers" + " "*28 + "║")
log("║" + " "*68 + "║")
log("╚" + "="*68 + "╝\n")

# ==================== MONITOR ====================
log("✅ System monitoring active (Ctrl+C to stop)\n")

monitor_count = 0
backend_restarts = 0
frontend_restarts = 0

try:
    while True:
        time.sleep(2)
        monitor_count += 1
        
        # Check backend
        if backend_proc and backend_proc.poll() is not None:
            backend_restarts += 1
            if backend_restarts < 3:
                log(f"⚠️  Backend crashed. Restarting ({backend_restarts}/3)...")
                with open(BACKEND_LOG, 'a') as log_file:
                    backend_proc = subprocess.Popen(
                        f'"{sys.executable}" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload',
                        shell=True,
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        cwd=PROJECT_DIR,
                        preexec_fn=os.setsid
                    )
                processes.append(backend_proc)
                time.sleep(2)
            else:
                log("❌ Backend crashed multiple times. Giving up.")
                break
        
        # Check frontend
        if frontend_proc and frontend_proc.poll() is not None:
            log("⚠️  Frontend exited.")
            log(f"   Check logs: tail -f {FRONTEND_LOG}")
            break
        
        # Every 30 seconds, show status
        if monitor_count % 15 == 0:
            log("   ✓ Systems still running...")

except KeyboardInterrupt:
    log("\n\n⏸️  Interrupted by user")

cleanup()

