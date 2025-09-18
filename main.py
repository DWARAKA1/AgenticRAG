
from dotenv import load_dotenv
load_dotenv()  # This must be the first line
import subprocess
import sys
from app.templates.application import app  # or your actual entry point

def main():
    """Run the AgenticRAG Streamlit application"""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app/templates/application.py"])
    except Exception as e:
        print(f"Error running Streamlit app: {e}")
        print("Fallback: Running basic version...")
        # Provide dummy environ and start_response for WSGI app
        def start_response(status, headers):
            print(f"Status: {status}")
            print(f"Headers: {headers}")
        environ = {}
        app(environ, start_response)

if __name__ == "__main__":
    main()
