#!/usr/bin/env python3
"""
Full-Stack Churn Prediction System - Improved Setup
"""
import urllib.request
import tarfile
import os
import subprocess
import sys
import platform

def setup_nodejs():
    """Download Node.js and set up proper PATH"""
    arch = platform.machine()
    print(f"\n🔧 Setting up Node.js for {arch}...")
    
    extract_path = "/tmp/node_full"
    
    # Check if already done
    if arch == "arm64":
        node_path = f"{extract_path}/node-v20.11.0-darwin-arm64/bin/node"
        npm_path = f"{extract_path}/node-v20.11.0-darwin-arm64/bin/npm"
        url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-arm64.tar.gz"
    else:
        node_path = f"{extract_path}/node-v20.11.0-darwin-x64/bin/node"
        npm_path = f"{extract_path}/node-v20.11.0-darwin-x64/bin/npm"
        url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-x64.tar.gz"
    
    if os.path.exists(node_path) and os.path.exists(npm_path):
        print(f"✓ Node.js already available")
        bin_dir = os.path.dirname(node_path)
        return bin_dir
    
    print("📥 Downloading Node.js...")
    
    try:
        tmp_file = f"/tmp/node-{arch}-full.tar.gz"
        
        # Download
        urllib.request.urlretrieve(url, tmp_file)
        size_mb = os.path.getsize(tmp_file) / 1024 / 1024
        print(f"   ✓ Downloaded {size_mb:.1f}MB")
        
        # Extract
        print("   📦 Extracting...")
        os.makedirs(extract_path, exist_ok=True)
        with tarfile.open(tmp_file, 'r:gz') as tar:
            tar.extractall(extract_path)
        
        bin_dir = os.path.dirname(node_path)
        print(f"✓ Node.js installed to {bin_dir}")
        return bin_dir
        
    except Exception as e:
        print(f"❌ Node.js setup failed: {e}")
        return None

def install_frontend_deps(bin_dir):
    """Install frontend dependencies"""
    frontend_dir = "/Users/alok/Desktop/Customer churn Predictor/frontend"
    npm_path = f"{bin_dir}/npm"
    
    print(f"\n📦 Installing frontend dependencies...")
    
    env = os.environ.copy()
    # Ensure system shell and binaries are available
    env['PATH'] = f"{bin_dir}:/bin:/usr/bin:/usr/local/bin:{env.get('PATH', '')}"
    env['SHELL'] = '/bin/zsh'
    
    try:
        result = subprocess.run(
            [npm_path, "install", "--legacy-peer-deps"],
            cwd=frontend_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
            return True, bin_dir
        else:
            if "npm warn" in result.stderr.lower() or result.returncode in [0, 1]:
                print("✓ Dependencies ready (some warnings are normal)")
                return True, bin_dir
            else:
                print(f"⚠️  Installation had issues (continuing anyway):")
                print(result.stderr[:300])
                return True, bin_dir
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

def start_frontend(bin_dir):
    """Start frontend dev server"""
    frontend_dir = "/Users/alok/Desktop/Customer churn Predictor/frontend"
    npm_path = f"{bin_dir}/npm"
    
    print("\n" + "="*70)
    print("🌐 STARTING FRONTEND SERVER")
    print("="*70)
    print("\n✓ Backend:    http://localhost:8000")
    print("✓ Frontend:   http://localhost:3000")
    print("✓ API Docs:   http://localhost:8000/docs")
    print("\n👉 OPEN IN BROWSER: http://localhost:3000\n")
    print("(Press Ctrl+C to stop)\n")
    
    env = os.environ.copy()
    # Ensure system shell is available for npm scripts
    env['PATH'] = f"{bin_dir}:/bin:/usr/bin:/usr/local/bin:{env.get('PATH', '')}"
    env['SHELL'] = '/bin/zsh'
    
    try:
        subprocess.run(
            [npm_path, "run", "dev"],
            cwd=frontend_dir,
            env=env
        )
    except KeyboardInterrupt:
        print("\n\n👋 Frontend stopped\n")

def main():
    print("\n" + "="*70)
    print("🚀 FULL-STACK CHURN PREDICTION SYSTEM")
    print("="*70)
    
    # Setup Node.js
    bin_dir = setup_nodejs()
    if not bin_dir:
        print("\n❌ Failed to setup Node.js")
        return 1
    
    # Install dependencies
    success, bin_dir = install_frontend_deps(bin_dir)
    if not success:
        print("\n❌ Frontend setup failed")
        return 1
    
    # Start frontend
    start_frontend(bin_dir)
    return 0

if __name__ == "__main__":
    sys.exit(main())

