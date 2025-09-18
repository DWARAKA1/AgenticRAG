#!/usr/bin/env python3
"""
Simple test script to verify the AgenticRAG system components
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.components.data_loader import load_pdf_files, create_text_chunks, process_and_store_pdfs
from app.components.embeddings import get_embedding_model
from app.components.llm import load_llm_model
from app.common.logger import get_logger

logger = get_logger(__name__)

def test_components():
    """Test all system components"""
    print("Testing AgenticRAG Components\n")
    
    # Test 1: Document Loading
    print("1. Testing document loading...")
    try:
        documents = load_pdf_files()
        print(f"SUCCESS: Loaded {len(documents)} documents")
    except Exception as e:
        print(f"FAILED: Document loading failed: {e}")
        return False
    
    # Test 2: Text Chunking
    print("\n2. Testing text chunking...")
    try:
        chunks = create_text_chunks(documents)
        print(f"SUCCESS: Created {len(chunks)} text chunks")
    except Exception as e:
        print(f"FAILED: Text chunking failed: {e}")
        return False
    
    # Test 3: Embedding Model
    print("\n3. Testing embedding model...")
    try:
        embedding_model = get_embedding_model()
        print("SUCCESS: Embedding model loaded successfully")
    except Exception as e:
        print(f"FAILED: Embedding model failed: {e}")
        return False
    
    # Test 4: LLM Model
    print("\n4. Testing LLM model...")
    try:
        llm = load_llm_model()
        print("SUCCESS: LLM model loaded successfully")
    except Exception as e:
        print(f"FAILED: LLM model failed: {e}")
        return False
    
    # Test 5: Vector Store Creation
    print("\n5. Testing vector store creation...")
    try:
        process_and_store_pdfs()
        print("SUCCESS: Vector store created successfully")
    except Exception as e:
        print(f"FAILED: Vector store creation failed: {e}")
        return False
    
    print("\nAll tests passed! System is ready to use.")
    return True

if __name__ == "__main__":
    success = test_components()
    sys.exit(0 if success else 1)