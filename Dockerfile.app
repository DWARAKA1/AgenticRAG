FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY data/ ./data/
COPY main.py .

# Create necessary directories
RUN mkdir -p vectorstore logs

# Expose Streamlit port
EXPOSE 8501

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the application
CMD ["streamlit", "run", "app/templates/application.py", "--server.port=8501", "--server.address=0.0.0.0"]