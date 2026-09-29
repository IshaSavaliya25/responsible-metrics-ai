FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install frontend dependencies
RUN pip install --no-cache-dir \
    streamlit>=1.32.0 \
    pandas>=2.2.0 \
    plotly>=5.19.0 \
    requests>=2.31.0

# Copy application source
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit interface
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
