"""Multi-agent RAG orchestration with LangGraph."""
import logging
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
import os

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """State for multi-agent workflow."""
    messages: List[BaseMessage]
    source: str
    context: str

class MultiAgentRAG:
    """Orchestrates RAG, web search, and LLM for intelligent question answering."""
    
    def __init__(self, retriever, llm_model: str = "llama2-70b-4096"):
        self.retriever = retriever
        self.llm = ChatGroq(model=llm_model, temperature=0)
        self.web_search = DuckDuckGoSearchRun()
        
    def should_use_web_search(self, question: str) -> bool:
        """Decide if web search is needed."""
        web_keywords = ["latest", "current", "today", "recent", "news", "weather"]
        return any(kw in question.lower() for kw in web_keywords)
    
    def route(self, question: str) -> str:
        """Route query to RAG or web search."""
        return "web_search" if self.should_use_web_search(question) else "rag"
    
    def retrieve_context(self, question: str) -> str:
        """Get context from RAG."""
        try:
            docs = self.retriever.invoke(question, k=3)
            return "\n".join([d.page_content for d in docs])
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return ""
    
    def search_web(self, question: str) -> str:
        """Get context from web search."""
        try:
            results = self.web_search.run(question)
            return str(results)[:1000]
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return ""
    
    def generate_answer(self, question: str, context: str) -> str:
        """Generate answer using LLM with context."""
        prompt = f"""Based on the following context, answer the question.
        
Context:
{context}

Question: {question}

Answer:"""
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return "Unable to generate answer."
    
    def process(self, question: str) -> dict:
        """Process question through multi-agent workflow."""
        route = self.route(question)
        logger.info(f"Routing question to: {route}")
        
        if route == "web_search":
            context = self.search_web(question)
            source = "web"
        else:
            context = self.retrieve_context(question)
            source = "rag"
        
        answer = self.generate_answer(question, context)
        
        return {
            "question": question,
            "answer": answer,
            "source": source,
            "context_preview": context[:200] if context else "No context found"
        }
