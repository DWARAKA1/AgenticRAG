# AgenticRAG - End-to-End RAG System

A complete Retrieval-Augmented Generation (RAG) system built with LangChain, Groq, and Streamlit.

## Features

- 📄 **Document Processing**: Load and process PDF and text documents
- 🔍 **Intelligent Retrieval**: Vector-based document search using ChromaDB
- 🤖 **AI-Powered Answers**: Generate contextual answers using Groq's Llama models
- 🌐 **Web Interface**: User-friendly Streamlit application
- 🔒 **Local Processing**: All data stays on your machine

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd AgenticRAG

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file with your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Add Documents

Place your PDF or text files in the `data/` directory.

### 4. Run the Application

```bash
python main.py
```

Or run Streamlit directly:

```bash
streamlit run app/templates/application.py
```

## Usage

1. **Process Documents**: Click "Process PDFs" in the sidebar to create the vector store
2. **Ask Questions**: Use the chat interface to ask questions about your documents
3. **Get Answers**: The system will provide contextual answers based on your documents

## Project Structure

```
AgenticRAG/
├── app/
│   ├── common/           # Utilities (logging, exceptions)
│   ├── components/       # Core RAG components
│   ├── config/          # Configuration settings
│   └── templates/       # Streamlit application
├── data/               # Document storage
├── vectorstore/        # Vector database storage
├── logs/              # Application logs
└── main.py           # Entry point
```

## Configuration

Key settings in `app/config/config.py`:

- `CHUNK_SIZE`: Text chunk size for processing (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `EMBEDDING_MODEL`: HuggingFace embedding model
- `GROQ_MODEL`: Groq LLM model to use

## API Keys

Get your free API key from [Groq](https://console.groq.com/keys) and add it to your `.env` file.

## Troubleshooting

- Ensure all dependencies are installed
- Check that your API key is valid
- Verify documents are in the `data/` directory
- Check logs in the `logs/` directory for detailed error information

## License

MIT License - see LICENSE file for details.