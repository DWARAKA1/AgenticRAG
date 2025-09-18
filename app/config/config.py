import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Paths
DB_PINECONE_PATH = "vectorstore/chroma"
DATA_PATH = "data/"

# Chunking Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Model Configuration
GROQ_MODEL = "mixtral-8x7b-32768"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ChromaDB Configuration
CHROMA_COLLECTION_NAME = "agentic-rag"
EMBEDDING_DIMENSION = 384
