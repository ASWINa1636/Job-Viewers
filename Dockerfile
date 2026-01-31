FROM python:3.10-slim

# Install system dependencies (Tesseract OCR)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=backend/app.py

# Expose Flask port
EXPOSE 5000

# Run with Gunicorn (production server)
CMD ["gunicorn", "backend.app:app", "-b", "0.0.0.0:5000"]
