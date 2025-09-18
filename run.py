#!/usr/bin/env python3
"""
Simple runner script for the AgenticRAG system
"""

import subprocess
import sys
import os

def run_streamlit():
    """Run the Streamlit application"""
    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "app/templates/application.py", "--server.port", "8501"]
        print("Starting AgenticRAG System...")
        print("Open your browser to: http://localhost:8501")
        print("Press Ctrl+C to stop the server\n")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\nShutting down AgenticRAG System...")
    except Exception as e:
        print(f"Error starting the application: {e}")
        print("Try running: python -m streamlit run app/templates/application.py")

if __name__ == "__main__":
    run_streamlit()