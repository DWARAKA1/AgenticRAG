#!/usr/bin/env python3
"""Quick health check for AgenticRAG system"""

import os
import sys

def health_check():
    print("=== AgenticRAG Health Check ===\n")
    
    # Check environment
    print("1. Environment Check:")
    from app.config.config import GROQ_API_KEY
    print(f"   - GROQ_API_KEY: {'OK' if GROQ_API_KEY else 'MISSING'}")
    
    # Check directories
    print("\n2. Directory Check:")
    dirs = ['data', 'vectorstore', 'logs']
    for d in dirs:
        exists = os.path.exists(d)
        print(f"   - {d}/: {'EXISTS' if exists else 'MISSING'}")
    
    # Check sample data
    print("\n3. Sample Data Check:")
    sample_file = "data/sample_document.txt"
    exists = os.path.exists(sample_file)
    print(f"   - Sample document: {'FOUND' if exists else 'MISSING'}")
    
    # Test imports
    print("\n4. Import Check:")
    try:
        from app.components.embeddings import get_embedding_model
        print("   - Embeddings: OK")
    except Exception as e:
        print(f"   - Embeddings: ERROR - {e}")
    
    try:
        from app.components.llm import load_llm_model
        print("   - LLM: OK")
    except Exception as e:
        print(f"   - LLM: ERROR - {e}")
    
    try:
        from app.templates.application import main
        print("   - Streamlit App: OK")
    except Exception as e:
        print(f"   - Streamlit App: ERROR - {e}")
    
    print("\n=== Health Check Complete ===")
    print("\nTo run the application:")
    print("  streamlit run app/templates/application.py")

if __name__ == "__main__":
    health_check()