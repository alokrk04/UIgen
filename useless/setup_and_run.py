#!/usr/bin/env python3
"""
Setup and run the full-stack churn prediction system
"""
import urllib.request
import tarfile
import os
import platform
import subprocess
import sys
import time

def download_nodejs():
    """Download and extract Node.js"""
    arch = platform.machine()
    print(f"🔧 System architecture: {arch}")
    
    if arch == "arm64":
        url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-arm64.tar.gz"
        filename = "node-v20.11.0-darwin-arm64.tar.gz"
    else:
        url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-x64.tar.gz"
        filename = "node-v20.11.0-darwin-x64.tar.gz"
    
    filepath = f"/tmp/{filename}"
    extract_path = "/tmp/node_extracted"
    
    try:
        if not os.path.exists(f"{extract_path}/node-v20.11.0-darwin-{arch}/bin/node"):
            print("📥 Downloading Node.js...")
            urllib.request.urlretrieve(url, filepath)
            print(f"✓ Downloaded")
            
            print("📦 Extracting...")
            os.makedirs(extract_path, exist_ok=True)
            with tarfile.open(filepath, 'r:gz') as tar:
                tar.extractall(extract_path)
            print(f"✓ Extracted")
        
        # Find node executable
        node_path = f"{extract_path}/node-v20.11.0-darwin-{arch}/bin/node"
        npm_path = f"{extract_path}/node-v20.11.0-darwin-{arch}/bin/npm"
        
        if os.path.exists(node_path):
            print(f"✓ Node found at: {node_path}")
            return node_path, npm_path
        else:
            print(f"❌ Node not found at {node_path}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

def main():
    print("\n" + "="*70)
    print("🚀 STARTING FULL-STACK CHURN PREDICTION SYSTEM")
    print("="*70 + "\n")
    
    # Setup Node.js
    node_path, npm_path = download_nodejs()
    
    if not node_path:
        print("\n❌ Could not set up Node.js")
        print("Please install Node.js manually from https://nodejs.org")
        sys.exit(1)
    
    # Setup NODE_PATH for this process
    os.environ['NODE_PATH'] = f"{os.path.dirname(node_path)}:../lib/node_modules"
    os.environ['PATH'] = f"{os.path.dirname(node_path)}:{os.path.dirname(npm_path)}:{os.environ.get('PATH', '')}"
    
    proj_dir = "/Users/alok/Desktop/Customer churn Predictor"
    frontend_dir = f"{proj_dir}/frontend"
    
    # Install frontend dependencies
    print(f"\n📦 Installing frontend dependencies...")
    try:
        result = subprocess.run(
            [npm_path, "install"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("✓ Frontend dependencies installed")
        else:
            print(f"⚠️  npm install output: {result.stderr}")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
    
    # Start frontend
    print(f"\n🌐 Starting frontend on port 3000...")
    print(f"To see the app, open: http://localhost:3000\n")
    
    try:
        subprocess.run(
            [npm_path, "run", "dev"],
            cwd=frontend_dir
        )
    except KeyboardInterrupt:
        print("\n\n👋 Frontend stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

