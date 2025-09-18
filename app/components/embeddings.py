
from langchain_huggingface import HuggingFaceEmbeddings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import EMBEDDING_MODEL

logger = get_logger(__name__)

def get_embedding_model():
    try:
        logger.info("Initializing the embedding model....")
        model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        logger.info("Embedding model initialized successfully....")
        return model
    except Exception as e:
        error_message = CustomException("Failed to initialize the embedding model", e)
        logger.error(str(error_message))
        raise error_message
