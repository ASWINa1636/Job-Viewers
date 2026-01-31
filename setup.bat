@echo off
REM Job Viewers - Windows Setup Script
REM This script automates the setup process on Windows

echo ==========================================
echo Job Viewers - Automated Setup (Windows)
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo pip upgraded
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Download spaCy model
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm
echo spaCy model downloaded
echo.

REM Create necessary directories
echo Creating directories...
if not exist "uploads" mkdir uploads
if not exist "templates" mkdir templates
if not exist "static" mkdir static
echo Directories created
echo.

REM Check for Tesseract
echo Checking for Tesseract OCR...
where tesseract >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Tesseract found
    tesseract --version
) else (
    echo WARNING: Tesseract OCR not found!
    echo Please install Tesseract manually:
    echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo After installation, add to PATH: C:\Program Files\Tesseract-OCR
)
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the app: python app.py
echo   3. Open browser: http://localhost:5000
echo.
pause