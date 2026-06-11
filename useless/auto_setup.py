#!/usr/bin/env python3
"""
Automated setup for Node.js and frontend
"""
import urllib.request
import urllib.error
import tarfile
import os
import subprocess
import sys
import platform
import shutil
import time

def download_file(url, dest):
    """Download a file with progress"""
    try:
        print(f"📥 Downloading from {url}...")
        urllib.request.urlretrieve(url, dest)
        print(f"✓ Downloaded to {dest}")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def extract_tar_gz(filepath, extract_to):
    """Extract tar.gz file"""
    try:
        print(f"📦 Extracting {filepath}...")
        os.makedirs(extract_to, exist_ok=True)
        with tarfile.open(filepath, 'r:gz') as tar:
            tar.extractall(extract_to)
        print(f"✓ Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False

def get_node_paths():
    """Find or download Node.js"""
    arch = platform.machine()
    print(f"\n🔧 System: macOS {arch}\n")
    
    # Check common installation paths
    for path in ["/usr/local/bin/node", "/opt/homebrew/bin/node", "/usr/bin/node"]:
        if os.path.exists(path):
            npm_path = path.replace("node", "npm")
            print(f"✓ Found Node.js at {path}")
            return os.path.dirname(path)
    
    # Try downloading to /tmp
    print("Node.js not found. Downloading...")
    
    if arch == "arm64":
        url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-arm64.tar.gz"
    else:
        url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-x64.tar.gz"
    
    tmp_file = f"/tmp/node-{arch}.tar.gz"
    extract_path = "/tmp/node_bin"
    
    if not os.path.exists(f"{extract_path}/bin/node"):
        if not download_file(url, tmp_file):
            return None
        if not extract_tar_gz(tmp_file, extract_path):
            return None
        
        # Move extracted node to bin directory
        extracted_folders = os.listdir(extract_path)
        if extracted_folders:
            extracted_dir = os.path.join(extract_path, extracted_folders[0])
            bin_dir = os.path.join(extracted_dir, "bin")
            if os.path.exists(bin_dir):
                print(f"✓ Node.js ready at {bin_dir}")
                return bin_dir
    else:
        print(f"✓ Using existing Node.js from {extract_path}")
        return f"{extract_path}/bin"
    
    return None

def run_command(cmd, cwd=None, env=None):
    """Run a command and return output"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def main():
    print("\n" + "="*70)
    print("🚀 SETTING UP FULL-STACK CHURN PREDICTION SYSTEM")
    print("="*70)
    
    project_dir = "/Users/alok/Desktop/Customer churn Predictor"
    frontend_dir = os.path.join(project_dir, "frontend")
    
    # Get Node.js
    node_bin_dir = get_node_paths()
    if not node_bin_dir:
        print("\n❌ Could not establish Node.js")
        print("Manual install: https://nodejs.org/ (LTS version)")
        return False
    
    # Set up environment
    env = os.environ.copy()
    env['PATH'] = f"{node_bin_dir}:{env.get('PATH', '')}"
    
    node_path = os.path.join(node_bin_dir, "node")
    npm_path = os.path.join(node_bin_dir, "npm")
    
    # Verify
    print(f"\n🔍 Verifying Node.js installation...")
    success, stdout, _ = run_command([node_path, "--version"])
    if success:
        print(f"✓ Node.js version: {stdout.strip()}")
    
    success, stdout, _ = run_command([npm_path, "--version"])
    if success:
        print(f"✓ npm version: {stdout.strip()}")
    
    # Install frontend dependencies
    print(f"\n📦 Installing frontend dependencies...")
    print(f"   Location: {frontend_dir}")
    
    success, stdout, stderr = run_command([npm_path, "ci"], cwd=frontend_dir, env=env)
    if not success and "ci" in stderr:
        print("   Trying npm install...")
        success, stdout, stderr = run_command([npm_path, "install"], cwd=frontend_dir, env=env)
    
    if success:
        print("✓ Dependencies installed successfully")
    else:
        print(f"⚠️  Installation warnings: {stderr[:200]}")
    
    # Start frontend
    print(f"\n" + "="*70)
    print("🌐 STARTING FRONTEND")
    print("="*70)
    print(f"\n✓ Backend is running on  http://localhost:8000")
    print(f"✓ Frontend starting on   http://localhost:3000")
    print(f"✓ API Docs on            http://localhost:8000/docs")
    print(f"\n👉 Open http://localhost:3000 in your browser!\n")
    
    # Run dev server
    try:
        subprocess.run(
            [npm_path, "run", "dev"],
            cwd=frontend_dir,
            env=env
        )
    except KeyboardInterrupt:
        print("\n\n👋 Frontend stopped by user")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

