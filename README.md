# Job Viewers

## Overview

Job Viewers is a comprehensive web-based application that allows users to upload their resumes, extract relevant skills using NLP, and get personalized job recommendations. The platform also includes a job posting system with user authentication.

## Features

✅ **Resume Upload & Parsing**: Supports PDF, DOCX, and images (PNG, JPG, JPEG) with OCR  
✅ **Skill Extraction**: Uses NLP (spaCy, PhraseMatcher) to extract skills automatically  
✅ **Job Recommendations**: Matches extracted skills with available job listings  
✅ **User Authentication**: Secure signup, login, and logout system  
✅ **Company Profiles**: Create detailed company profiles with full information  
✅ **Job Posting**: Authenticated users can post job listings with application links  
✅ **Job Management**: Edit and delete your own job postings  
✅ **Apply Button**: Direct application links on each job posting  
✅ **Job Types**: Full-time, Part-time, Contract, Internship, Freelance  
✅ **Experience Levels**: Entry-level, Mid-level, Senior, Lead, Executive  
✅ **Database**: SQLite for job-related data and user authentication  
✅ **Responsive Design**: Beautiful, modern UI with gradient backgrounds  

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **NLP**: spaCy, PhraseMatcher
- **File Processing**: PyMuPDF, python-docx, Tesseract OCR
- **Security**: Werkzeug password hashing

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (for image processing)

### Step 1: Install Tesseract OCR

**Windows:**
```bash
# Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH: C:\Program Files\Tesseract-OCR
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Step 2: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd job-viewers

# Or simply extract the downloaded files to a folder
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

## Project Structure

```
Job-Viewers/
├── .gitignore                    ← Git ignore file
├── LICENSE                       ← MIT License
├── README.md                     ← Main documentation
├── requirements.txt              ← Python dependencies
├── setup.sh                      ← Linux/Mac setup
├── setup.bat                     ← Windows setup
├── Quickstart.md
├── CONTRIBUTING.md               ← (Optional) How to contribute
│
└── backend/
    ├── app.py                    ← Main application
    ├── migrate_database.py       ← Database setup
    │
    └── templates/                ← HTML templates
        ├── index.html
        ├── company_signup.html
        ├── company_login.html
        ├── company_dashboard.html
        ├── edit_company_profile.html
        ├── add_job.html
        └── edit_job.html
```

## Usage

### Starting the Application

```bash
# Make sure your virtual environment is activated
python app.py
```

The application will start on `http://localhost:5000`

### Using the Application

1. **Home Page**
   - Visit `http://localhost:5000`
   - Search for jobs by entering skills manually
   - Upload your resume (PDF, DOCX, or image) to extract skills automatically

2. **Sign Up**
   - Click on the menu icon (☰) → Sign Up
   - Enter username, email, and password
   - Create your account

3. **Login**
   - Click on the menu icon (☰) → Login
   - Enter your credentials
   - Access authenticated features

4. **Post a Job** (Requires Login)
   - Click on the menu icon (☰) → Add Job
   - Fill in job details: title, company, location, description, skills, salary
   - Submit to create a job listing

5. **Search for Jobs**
   - Enter skills manually in the search box
   - OR upload your resume to extract skills automatically
   - View matching job recommendations

## Features in Detail

### Resume Processing

The application can process multiple file formats:

- **PDF Files**: Extracts text using PyMuPDF
- **DOCX Files**: Extracts text and performs OCR on embedded images
- **Image Files**: Uses Tesseract OCR to extract text from images

### Skill Extraction

Uses spaCy's PhraseMatcher with a comprehensive list of 200+ technical and professional skills, including:
- Programming languages (Python, Java, JavaScript, C++, etc.)
- Frameworks (React, Django, Flask, Spring Boot, etc.)
- Technologies (AWS, Docker, Kubernetes, etc.)
- Soft skills (Team Leadership, Project Management, etc.)

### Job Matching Algorithm

- Compares extracted/entered skills with job requirements
- Case-insensitive matching
- Returns all jobs that match at least one skill
- Displays full job details including description, salary, and posting date

## Database Schema

### Users Table (security.db)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    user_type TEXT DEFAULT 'jobseeker'
);
```

### Company Profiles Table (security.db)
```sql
CREATE TABLE company_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    company_description TEXT,
    company_website TEXT,
    company_email TEXT,
    company_phone TEXT,
    company_address TEXT,
    industry TEXT,
    company_size TEXT,
    founded_year TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Jobs Table (database.db)
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT NOT NULL,  -- JSON array
    salary TEXT NOT NULL,
    date_posted TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    application_link TEXT,
    job_type TEXT,
    experience_level TEXT,
    UNIQUE(title, company, location)
);
```

## Security Features

- Password hashing using Werkzeug's `generate_password_hash`
- Session management with secure cookies
- Input validation and sanitization
- SQL injection prevention with parameterized queries
- XSS protection with HTML escaping

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   # Make sure all dependencies are installed
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Tesseract not found**
   ```bash
   # Install Tesseract OCR and add to PATH
   # Windows: Set environment variable
   # macOS/Linux: Tesseract should be in PATH after installation
   ```

3. **Database errors**
   ```bash
   # Delete existing databases and restart
   rm database.db security.db
   python app.py
   ```

4. **Port already in use**
   ```python
   # Change the port in app.py
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```

## Development

### Running in Debug Mode

Debug mode is enabled by default in `app.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

This provides:
- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger

### Adding New Skills

Edit the `SKILLS` list in `app.py` to add more skills to the recognition system.

## Contributing

Feel free to submit pull requests or open issues if you find bugs or have feature requests.

### Ideas for Future Enhancements

- Email verification for signups
- Password reset functionality
- Advanced job filtering (location, salary range, etc.)
- Employer dashboard
- Application tracking
- Resume builder
- Job application submission
- Email notifications
- Admin panel
- API endpoints

## License

MIT License

## Contact

For questions or support, please open an issue on the repository.

## Acknowledgments

- Built with Flask web framework
- NLP powered by spaCy
- OCR powered by Tesseract
- UI design inspired by modern web standards