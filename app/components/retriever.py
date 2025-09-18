from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm_model
from app.components.vector_store import load_vector_store

# from app.common.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """Answer the following question as best as you can using the provided context.

context:
{context}

Question: 
{question}

Answer:
"""

def set_custom_prompt():
    return  PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )


def create_qa_chain():
    try:
        logger.info("Creating the QA chain....")

        llm = load_llm_model()

        vector_store = load_vector_store()
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})

        prompt = set_custom_prompt()

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt":prompt}
        )

        logger.info("QA chain created successfully....")

        return qa_chain

    except Exception as e:
        error_message = CustomException("Failed to create the QA chain",e)
        logger.error(str(error_message))
        raise error_message