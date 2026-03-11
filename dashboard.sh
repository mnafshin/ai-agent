#!/bin/bash
# Start AI Agent Dashboard Server
# Usage: bash dashboard.sh

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║                                                      ║"
echo "║     Starting AI Agent Dashboard Server              ║"
echo "║                                                      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment if it exists
if [ -f .venv/bin/activate ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Warning: Virtual environment not found"
    echo "Run bash setup.sh first to create it"
    echo ""
fi

# Check if Flask is installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Flask not found. Installing dashboard dependencies..."
    pip install flask flask-cors
fi

# Start the dashboard server
cd agent_core
python dashboard_server.py

