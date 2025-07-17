#!/usr/bin/env python3
"""
Railway deployment start script for Face Recognition Server
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from server import app
    print("🚀 Starting Face Recognition Server...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)