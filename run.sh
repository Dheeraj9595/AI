#!/bin/bash

# Quick start script for the AI Studio application

echo "🚀 Starting AI Studio..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "🔐 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start the server
echo ""
echo "✨ Starting server..."
echo "🌐 Web Interface: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
