# Use Python 3.8.10 base image
FROM python:3.8.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libmagic1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download NLTK and spaCy resources
RUN python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger
RUN python -m spacy download en_core_web_sm

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "App.py", "--server.port=8501", "--server.address=0.0.0.0"]
