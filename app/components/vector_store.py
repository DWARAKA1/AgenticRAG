"""
This module provides functions to load and save vector stores using ChromaDB for retrieval-augmented generation.
"""
from langchain_chroma import Chroma
import os
from app.components.embeddings import get_embedding_model
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DB_PINECONE_PATH

logger = get_logger(__name__)

def load_vector_store():
    """
    Loads a ChromaDB vector store from the specified path if it exists.
    Returns:
        vector_store: The loaded ChromaDB vector store object.
    Raises:
        CustomException: If the vector store cannot be loaded or does not exist.
    """
    try:
        embedding_model = get_embedding_model()
        if os.path.exists(DB_PINECONE_PATH):
            logger.info("Loading the vector store from ChromaDB...")
            vector_store = Chroma(
                persist_directory=DB_PINECONE_PATH,
                embedding_function=embedding_model
            )
            logger.info("Vector store loaded successfully from ChromaDB.")
            return vector_store
        else:
            logger.error("ChromaDB index does not exist.")
            raise CustomException("ChromaDB index does not exist.")
    except Exception as e:
        logger.error(f"Error loading vector store: {e}")
        raise CustomException("Error loading vector store", e)

def save_vector_store(text_chunks):
    """
    Saves a new ChromaDB vector store from provided text chunks.
    Args:
        text_chunks (list): List of text chunks to embed and store.
    Returns:
        vector_store: The created ChromaDB vector store object.
    Raises:
        CustomException: If saving fails or no text chunks are provided.
    """
    try:
        if not text_chunks:
            logger.error("No text chunks provided for saving vector store.")
            raise CustomException("No text chunks provided for saving vector store.")
        logger.info("Creating a new vector store in ChromaDB...")
        embedding_model = get_embedding_model()
        vector_store = Chroma.from_texts(
            texts=text_chunks,
            embedding=embedding_model,
            persist_directory=DB_PINECONE_PATH
        )
        logger.info("Saving vector store.")
        # Auto-persisted in Chroma 0.4.x+
        logger.info("Vector store saved successfully.")
        return vector_store
    except Exception as e:
        error_message = CustomException("Failed to save the vector store", e)
        logger.error(str(error_message))
        raise error_message
