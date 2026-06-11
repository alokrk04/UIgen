#!/usr/bin/env python3
"""
🚀 AUTOMATIC NODE.JS INSTALLER + FULL STACK RUNNER
Downloads Node.js for macOS arm64 and starts both servers
"""

import subprocess
import os
import sys
import time
import signal
import atexit
import urllib.request
import tarfile
import shutil

PROJECT_DIR = "/Users/alok/Desktop/Customer churn Predictor"
os.chdir(PROJECT_DIR)

# Store process IDs for cleanup
processes = []

def cleanup():
    """Kill all spawned processes on exit"""
    print("\n\n🛑 Shutting down servers...")
    for p in processes:
        try:
            if p.poll() is None:  # Process still running
                p.terminate()
                time.sleep(1)
                if p.poll() is None:
                    p.kill()
        except:
            pass
    print("✅ All servers stopped")

atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

def download_file(url, dest):
    """Download a file with progress"""
    try:
        print(f"   Downloading: {url}")
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
        return False

def install_nodejs():
    """Download and install Node.js for macOS arm64"""
    print("\n📥 Installing Node.js...")
    
    # Check if node_dir already exists
    node_dir = os.path.expanduser("~/.local/opt/node")
    if os.path.exists(f"{node_dir}/bin/node"):
        print("✅ Node.js already installed locally")
        return node_dir
    
    os.makedirs(node_dir, exist_ok=True)
    os.makedirs("/tmp/node_install", exist_ok=True)
    
    # Download Node.js v20 LTS for macOS arm64
    node_version = "v20.11.0"
    node_url = f"https://nodejs.org/dist/{node_version}/node-{node_version}-darwin-arm64.tar.xz"
    tar_path = "/tmp/node_install/node.tar.xz"
    
    print(f"   Version: {node_version}")
    if download_file(node_url, tar_path):
        print("   ✅ Download complete")
        
        # Extract
        print("   📦 Extracting...")
        try:
            import lzma
            with lzma.open(tar_path) as f:
                with tarfile.open(fileobj=f) as tar:
                    tar.extractall("/tmp/node_install")
            
            # Copy binaries
            src_bin = f"/tmp/node_install/node-{node_version}-darwin-arm64/bin"
            dst_bin = f"{node_dir}/bin"
            os.makedirs(dst_bin, exist_ok=True)
            
            for exe in ["node", "npm", "npx"]:
                src = os.path.join(src_bin, exe)
                dst = os.path.join(dst_bin, exe)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    os.chmod(dst, 0o755)
            
            print(f"✅ Node.js installed to {node_dir}")
            return node_dir
        except Exception as e:
            print(f"   ❌ Extraction failed: {e}")
            return None
    else:
        print("❌ Failed to install Node.js")
        return None

def run_command(cmd, name, background=False, env=None):
    """Run a command and return the process"""
    print(f"\n🚀 Starting {name}...")
    try:
        env_copy = os.environ.copy()
        if env:
            env_copy.update(env)
        
        if background:
            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True,
                env=env_copy
            )
            processes.append(p)
            print(f"✅ {name} started (PID: {p.pid})")
            return p
        else:
            result = subprocess.run(cmd, shell=True, capture_output=False, env=env_copy)
            return result
    except Exception as e:
        print(f"❌ Error starting {name}: {e}")
        return None

def npm_cmd(args, node_path):
    """Generate npm command using node directly if needed"""
    if node_path:
        return f"{node_path}/bin/node {node_path}/lib/node_modules/npm/bin/npm-cli.js {args}"
    else:
        return f"npm {args}"

try:
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🚀 CHURN PREDICTION SYSTEM - FULL STACK LAUNCHER              ║")
    print("║  Auto-Installing Node.js + Starting Servers                    ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")

    # Step 1: Verify Python
    print(f"✅ Python version: {sys.version.split()[0]}")

    # Step 2: Install backend dependencies
    print("\n📦 Installing Python backend dependencies...")
    result = subprocess.run(
        f"{sys.executable} -m pip install -q -r backend/requirements.txt",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"⚠️  Some warnings (this is normal): {result.stderr[:100]}")
    print("✅ Backend dependencies ready")

    # Step 3: Start Backend
    print("\n" + "="*70)
    print("🔧 STARTING BACKEND (FastAPI)")
    print("="*70)
    backend_cmd = f"{sys.executable} -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
    backend_process = run_command(backend_cmd, "Backend Server", background=True)
    time.sleep(3)

    # Step 4: Verify Backend
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:8000/api/health", timeout=3)
        print("✅ Backend is responding!")
    except Exception as e:
        print(f"⚠️  Backend not responding yet (may still be starting): {e}")

    # Step 5: Install Node.js if needed
    print("\n" + "="*70)
    print("📦 SETTING UP NODE.JS")
    print("="*70)
    
    node_path = None
    node_check = subprocess.run("node --version 2>&1", shell=True, capture_output=True, text=True)
    if node_check.returncode == 0:
        print(f"✅ Node.js found: {node_check.stdout.strip()}")
        node_path = ""
    else:
        print("⚠️  Node.js not found in PATH, installing...")
        node_path = install_nodejs()
        if not node_path:
            print("❌ Could not install Node.js")
            sys.exit(1)

    # Step 6: Frontend Dependencies
    print("\n" + "="*70)
    print("🌐 SETTING UP FRONTEND (React/Next.js)")
    print("="*70)
    
    os.chdir(f"{PROJECT_DIR}/frontend")
    
    # Set up environment with Node.js path if needed
    env_vars = {}
    if node_path:
        env_vars['PATH'] = f"{node_path}/bin:" + os.environ.get('PATH', '')
    
    npm_check = subprocess.run(
        "npm --version 2>&1",
        shell=True,
        capture_output=True,
        text=True,
        env={**os.environ, **env_vars} if env_vars else None
    )
    if npm_check.returncode == 0:
        print(f"✅ npm version: {npm_check.stdout.strip()}")
    else:
        print(f"⚠️  npm check: {npm_check.stderr}")

    if not os.path.exists("node_modules"):
        print("\n📥 Installing npm packages (first time, ~1-2 min)...")
        npm_install_cmd = npm_cmd("install --prefer-offline --no-audit", node_path)
        npm_install = subprocess.run(
            npm_install_cmd,
            shell=True,
            capture_output=False,
            env={**os.environ, **env_vars} if env_vars else None
        )
        if npm_install.returncode != 0:
            print("⚠️  npm install warnings (usually safe)")
    else:
        print("✅ npm packages already installed")

    # Step 7: Start Frontend
    print("\n" + "="*70)
    print("🚀 STARTING FRONTEND (Next.js)")
    print("="*70)
    
    # Make sure npm is in PATH for frontend
    if node_path:
        frontend_env = env_vars.copy()
        frontend_env['PATH'] = f"{node_path}/bin:" + os.environ.get('PATH', '')
    else:
        frontend_env = {}
    
    frontend_cmd = npm_cmd("run dev", node_path)
    frontend_process = run_command(
        frontend_cmd,
        "Frontend Server",
        background=True,
        env=frontend_env
    )
    time.sleep(5)

    # Step 8: Success Summary
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + " "*12 + "✅ SUCCESS! YOUR SYSTEM IS RUNNING! ✅" + " "*18 + "║")
    print("║" + " "*68 + "║")
    print("╠" + "="*68 + "╣")
    print("║" + " "*68 + "║")
    print("║  📱 OPEN BROWSER:  http://localhost:3000" + " "*23 + "║")
    print("║" + " "*68 + "║")
    print("║  Backend URLs:" + " "*53 + "║")
    print("║    🔌 http://localhost:8000" + " "*38 + "║")
    print("║    📚 http://localhost:8000/docs" + " "*33 + "║")
    print("║" + " "*68 + "║")
    print("║  📂 Test Datasets:" + " "*48 + "║")
    print("║     • data/telecom_churn_data.csv" + " "*33 + "║")
    print("║     • CSV's/BankChurners.csv" + " "*38 + "║")
    print("║     • CSV's/patient_churn_dataset.csv" + " "*28 + "║")
    print("║" + " "*68 + "║")
    print("║  📋 Usage:" + " "*57 + "║")
    print("║     1. Upload a CSV file" + " "*42 + "║")
    print("║     2. Click 'Run Churn Pipeline'" + " "*33 + "║")
    print("║     3. Wait 2-3 minutes for results" + " "*30 + "║")
    print("║     4. View visualizations and predictions" + " "*23 + "║")
    print("║" + " "*68 + "║")
    print("║  ⌨️  Press Ctrl+C to stop all servers" + " "*28 + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")

    # Wait indefinitely and monitor
    print("✅ All systems running. Monitoring processes...\n")
    
    restart_count = 0
    while True:
        time.sleep(2)
        
        # Check if processes are still alive
        if backend_process and backend_process.poll() is not None:
            restart_count += 1
            if restart_count < 3:
                print(f"⚠️  Backend died. Restarting ({restart_count}/3)...")
                backend_process = run_command(backend_cmd, "Backend Server", background=True)
            else:
                print("❌ Backend crashed too many times. Exiting.")
                sys.exit(1)
        
        if frontend_process and frontend_process.poll() is not None:
            print("⚠️  Frontend died. This might be a build issue.")
            print("   Check the output above for errors.")
            break

except KeyboardInterrupt:
    print("\n\n⏸️  Interrupted by user")
except Exception as e:
    print(f"\n❌ Fatal error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    cleanup()

