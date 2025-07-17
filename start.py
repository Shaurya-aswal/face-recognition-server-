#!/usr/bin/env python3
"""
Railway deployment start script for Face Recognition Server
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and start the server
if __name__ == "__main__":
    import server
    print("🚀 Starting Face Recognition Server on Railway...")
