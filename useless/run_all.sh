#!/bin/zsh

# Full-stack Churn Prediction System - Run Script

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🚀  RUNNING FULL-STACK CHURN PREDICTION SYSTEM"
echo "════════════════════════════════════════════════════════════════"
echo ""

PROJECT_DIR="/Users/alok/Desktop/Customer churn Predictor"
BACKEND_DIR="$PROJECT_DIR"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "📍 Project directory: $PROJECT_DIR"
echo ""

# Check if backend is already running
echo "🔍 Checking if backend is running on port 8001..."
if curl -s http://localhost:8001/api/health > /dev/null 2>&1; then
    echo "✓ Backend is already running on http://localhost:8001"
else
    echo "🚀 Starting backend on port 8001..."
    cd "$BACKEND_DIR"
    /usr/bin/python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload &
    BACKEND_PID=$!
    echo "✓ Backend started (PID: $BACKEND_PID)"
    sleep 3
fi

echo ""
echo "📦 Setting up frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Attempting to install..."

    # Try using existing Node.js from tmp if available
    if [ -f "/tmp/node_extracted/node-v20.11.0-darwin-arm64/bin/node" ]; then
        export PATH="/tmp/node_extracted/node-v20.11.0-darwin-arm64/bin:$PATH"
        echo "✓ Using extracted Node.js from /tmp"
    elif [ -f "/tmp/node_extracted/node-v20.11.0-darwin-x64/bin/node" ]; then
        export PATH="/tmp/node_extracted/node-v20.11.0-darwin-x64/bin:$PATH"
        echo "✓ Using extracted Node.js from /tmp"
    else
        echo "❌ Node.js required but not installed"
        echo "Please install Node.js from: https://nodejs.org/"
        exit 1
    fi
fi

# Verify node and npm
echo "Verifying Node.js installation..."
node --version
npm --version

echo ""
echo "📦 Installing frontend dependencies..."
cd "$FRONTEND_DIR"
npm install

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🌐 Starting Frontend on port 3000"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✓ Backend API:  http://localhost:8001"
echo "✓ Frontend:     http://localhost:3000"
echo "✓ Backend Docs: http://localhost:8001/docs"
echo ""
echo "👉 Open http://localhost:3000 in your browser!"
echo ""

npm run dev

