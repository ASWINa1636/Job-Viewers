# Quick Start Guide - Job Viewers

## 🚀 Fast Setup (5 minutes)

### 1. Install Prerequisites

**Install Tesseract OCR:**
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

### 2. Setup the Application

**Option A: Automatic Setup (Recommended)**

**On Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

**Option B: Manual Setup**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access the Application

Open your browser and go to: **http://localhost:5000**

## 📖 Basic Usage

### Creating an Account
1. Click the menu icon (☰) in the top-left corner
2. Click "Sign Up"
3. Fill in your details and create an account

### Finding Jobs
1. **Method 1**: Enter skills manually (e.g., "Python, Java, React")
2. **Method 2**: Upload your resume (PDF, DOCX, or image)
3. Click "Search" to see matching jobs

### Posting a Job (Login Required)
1. Login to your account
2. Click the menu icon (☰) → "Add Job"
3. Fill in the job details
4. Submit to create the job listing

## 🎯 Features

✅ Upload PDF, DOCX, or image resumes  
✅ Automatic skill extraction using AI  
✅ Smart job matching  
✅ Secure user authentication  
✅ Post job listings  
✅ Beautiful, responsive design  

## 🔧 Troubleshooting

**Issue: Can't find Tesseract**
- Make sure Tesseract is installed
- Add Tesseract to your system PATH

**Issue: Module not found**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Issue: Port already in use**
- Change port in app.py (line 397): `app.run(port=5001)`

## 📝 Default Test Credentials

For testing, you can create an account with any email and password.
There are no default credentials - you must sign up first.

## 🎨 Supported File Types

- **Resumes**: PDF, DOCX, PNG, JPG, JPEG
- **Max File Size**: 10 MB

## 💡 Tips

- Use clear, well-formatted resumes for best skill extraction
- Enter skills separated by commas when searching manually
- Login to access job posting features
- Check the extracted skills to verify accuracy

## 📧 Need Help?

Check the full README.md for detailed documentation and troubleshooting.

---

**Happy Job Hunting! 🎉**