"""Tool definitions for agent toolkit."""
from langchain_community.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool
from typing import List
import math

# Web search tool
web_search_tool = DuckDuckGoSearchRun()

@tool
def calculator(expression: str) -> float:
    """Evaluate a math expression."""
    try:
        return eval(expression, {"__builtins__": {}, "math": math})
    except Exception as e:
        return f"Error: {e}"

@tool
def get_context_from_docs(query: str) -> str:
    """Retrieve context from uploaded documents using semantic search."""
    # This will be injected by the app
    return "Document context will be retrieved here"

def setup_tools() -> List[Tool]:
    """Setup all available tools for the agent."""
    return [
        Tool(
            name="web_search",
            func=web_search_tool.run,
            description="Search the internet for recent information"
        ),
        calculator,
        get_context_from_docs
    ]
