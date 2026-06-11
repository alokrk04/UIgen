#!/usr/bin/env python3
import os, json, urllib.request

print("\n" + "="*70)
print("🔍 CHURN PREDICTION SYSTEM - RUNTIME STATUS")
print("="*70 + "\n")

status = {}

# Check Node.js download
node_path = "/tmp/node_full/node-v20.11.0-darwin-arm64/bin/node"
if not os.path.exists(node_path):
    node_path = "/tmp/node_full/node-v20.11.0-darwin-x64/bin/node"
status["Node.js"] = "✓ Downloaded" if os.path.exists(node_path) else "⏳ Downloading..."

# Check frontend dependencies
node_modules = "/Users/alok/Desktop/Customer churn Predictor/frontend/node_modules"
status["Frontend Deps"] = "✓ Installed" if os.path.exists(node_modules) else "⏳ Installing..."

# Check Backend
try:
    r = urllib.request.urlopen('http://localhost:8000/api/health', timeout=2)
    data = json.loads(r.read().decode())
    status["Backend API"] = f"✓ Running (port 8000)"
except:
    status["Backend API"] = "❌ Not running"

# Check Frontend
try:
    r = urllib.request.urlopen('http://localhost:3000', timeout=2)
    status["Frontend"] = "✓ Running (port 3000)"
except:
    status["Frontend"] = "⏳ Starting or not ready..."

for key, val in status.items():
    print(f"  {key:20} {val}")

print("\n" + "="*70)
print("📝 INSTRUCTIONS")
print("="*70 + "\n")
print("  1️⃣  Both servers must be running")
print("  2️⃣  Open: http://localhost:3000")
print("  3️⃣  Upload a CSV file to test")
print("\n  To stop: Press Ctrl+C in the terminal\n")
print("="*70 + "\n")

