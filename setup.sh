#!/bin/bash

# Job Viewers - Setup Script
# This script automates the setup process

echo "=========================================="
echo "Job Viewers - Automated Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Download spaCy model
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm
echo "✓ spaCy model downloaded"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads templates static
echo "✓ Directories created"
echo ""

# Check for Tesseract
echo "Checking for Tesseract OCR..."
if command -v tesseract &> /dev/null
then
    tesseract_version=$(tesseract --version 2>&1 | head -n 1)
    echo "✓ Tesseract found: $tesseract_version"
else
    echo "⚠ WARNING: Tesseract OCR not found!"
    echo "Please install Tesseract manually:"
    echo "  - macOS: brew install tesseract"
    echo "  - Linux: sudo apt-get install tesseract-ocr"
    echo "  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""