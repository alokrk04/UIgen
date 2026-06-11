#!/bin/bash
# Complete Full-Stack Runner - Simple and Direct

PROJECT_DIR="/Users/alok/Desktop/Customer churn Predictor"
NODE_DIR="$HOME/.local/opt/node"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  🚀 CHURN PREDICTION SYSTEM - FULL STACK LAUNCHER              ║"
echo "║  Simple Direct Runner                                           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

cd "$PROJECT_DIR" || exit 1

# Kill any existing processes
pkill -f "uvicorn backend" 2>/dev/null || true
pkill -f "next dev" 2>/dev/null || true

# Sleep a bit
/usr/bin/python3 -c "import time; time.sleep(1)"

# Install backend dependencies
echo "📦 Installing Python dependencies..."
/usr/bin/python3 -m pip install -q -r backend/requirements.txt

# Start backend in background
echo "🔧 Starting Backend (FastAPI)..."
/usr/bin/python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload >/tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait for backend to start
/usr/bin/python3 -c "import time; time.sleep(3)"

# Start frontend
echo ""
echo "🌐 Starting Frontend (Next.js)..."
cd "$PROJECT_DIR/frontend"

# Export PATH with node
export PATH="$NODE_DIR/bin:$PATH"

# Run npm dev
/usr/bin/python3 -c "import time; time.sleep(1)"  # Small delay
/Users/alok/.local/opt/node/bin/node /Users/alok/.local/opt/node/lib/node_modules/npm/bin/npm-cli.js run dev


