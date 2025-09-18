from langchain_groq import ChatGroq
from app.config.config import GROQ_API_KEY
from pydantic import SecretStr

from app.common.logger import get_logger   
from app.common.custom_exception import CustomException

logger = get_logger(__name__)   

from typing import Optional

def load_llm_model(model_name: str = "llama-3.1-8b-instant", GROQ_API_KEY: Optional[str] = GROQ_API_KEY):
    try:
        if not GROQ_API_KEY:
            error_message = CustomException("GROQ_API_KEY is missing. Please set it in your environment or .env file.")
            logger.error(str(error_message))
            raise error_message
        logger.info("Loading LLM from GROQ using LLM model....")
        llm = ChatGroq(
            model=model_name,
            api_key=SecretStr(GROQ_API_KEY),
            temperature=0.3,
            max_retries=256,
        )
        logger.info("LLM model loaded from groq and initialized successfully....")
        return llm
    except Exception as e:
        error_message = CustomException("Failed to initialize the LLM model", e)
        logger.error(str(error_message))
        raise error_message