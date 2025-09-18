import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.components.vector_store import save_vector_store
from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_pdf_files():
    try:
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            logger.info(f"Created data directory: {DATA_PATH}")
            return []
        
        documents = []
        
        # Load PDF files
        try:
            pdf_loader = PyPDFDirectoryLoader(DATA_PATH)
            pdf_docs = pdf_loader.load()
            documents.extend(pdf_docs)
            logger.info(f"Loaded {len(pdf_docs)} PDF documents")
        except Exception as e:
            logger.warning(f"No PDF files found or error loading PDFs: {e}")
        
        # Load text files
        try:
            text_loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
            text_docs = text_loader.load()
            documents.extend(text_docs)
            logger.info(f"Loaded {len(text_docs)} text documents")
        except Exception as e:
            logger.warning(f"No text files found or error loading text files: {e}")
        
        logger.info(f"Total loaded {len(documents)} documents from {DATA_PATH}")
        return documents
    except Exception as e:
        logger.error(f"Error loading files: {e}")
        return []

def create_text_chunks(documents):
    if not documents:
        return ["Sample document text for testing purposes."]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} text chunks")
    return [chunk.page_content for chunk in chunks]

def process_and_store_pdfs():
    try:
        logger.info("Making the vector store....")
        documents = load_pdf_files()
        text_chunks = create_text_chunks(documents)
        save_vector_store(text_chunks)
        logger.info("Vector store created successfully....")
    except Exception as e:
        error_message = CustomException("Failed to create vector store", e)
        logger.error(str(error_message))


if __name__=="__main__":
    process_and_store_pdfs()