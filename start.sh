#!/bin/bash
echo "========================================"
echo "  MEDTRIAGE EXPERT SYSTEM"
echo "========================================"
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found."
    exit 1
fi
pip3 install flask flask-cors --quiet
echo "Starting server → http://localhost:5000"
python3 server.py
