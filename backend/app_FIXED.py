import os
import sqlite3
import fitz
import json
import pytesseract
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, g
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import docx
import spacy
from spacy.matcher import PhraseMatcher
from datetime import datetime
import io

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.secret_key = '98745632221478632156321489625'

AUTH_DATABASE_PATH = "security.db"
DATABASE_PATH = "database.db"

ALLOWED_EXTENSIONS = {"pdf", "docx", "png", "jpg", "jpeg"}

SKILLS = [
    "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Swift", "Kotlin", "TypeScript", "PHP", "Rust",
    "Scala", "Perl", "Haskell", "Lua", "Linux", "Windows", "macOS", "UNIX", "MATLAB", "Power Systems", "HTML", 
    "CSS", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring Boot", "ASP.NET", "Laravel",
    "Machine Learning", "Deep Learning", "Data Science", "TensorFlow", "PyTorch", "Keras", "Pandas", "NumPy", 
    "Scikit-Learn", "R", "Matplotlib", "Seaborn", "OpenAI API", "Natural Language Processing", "Computer Vision",
    "Big Data", "SQL", "PostgreSQL", "MongoDB", "Firebase", "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes",
    "Ethical Hacking", "Penetration Testing", "Cryptography", "Network Security", "SOC Analyst", "Malware Analysis",
    "Reverse Engineering", "CI/CD", "Jenkins", "Terraform", "Ansible", "Git", "GitHub Actions", "GitLab CI", 
    "Bash Scripting", "PowerShell", "Agile", "Scrum", "Kanban", "JIRA", "Trello", "Confluence", "PCB Design", 
    "Web Development", "Mobile Development", "Web developer", "Word", "Excel", "PowerPoint", "Outlook", "Tableau", "Power BI", 
    "Apache Spark", "Hadoop", "Kafka", "Elasticsearch", "GraphQL", "REST APIs", "SOAP", "Microservices", 
    "DevOps", "System Administration", "Virtualization", "VMware", "Hyper-V", "Cloud Security", "IoT", 
    "Embedded Systems", "Arduino", "Raspberry Pi", "Blockchain", "Solidity", "UI/UX Design", "UI/UX Engineer",
    "Figma", "Adobe XD", "Photoshop", "Illustrator", "Blender", "3D Modeling", "Game Development", "Unity", 
    "Unreal Engine", "OpenGL", "WebAssembly", "Quantum Computing", "Statistics", "Probability", "Linear Algebra", 
    "Data Visualization", "ETL Processes", "Data Warehousing", "Snowflake", "Redshift", "DynamoDB", "Cassandra", 
    "Neo4j", "Redis", "Load Balancing", "NGINX", "Apache", "Incident Response", "Forensic Analysis", "Threat Hunting", 
    "Cybersecurity Frameworks", "NIST", "ISO 27001", "GDPR Compliance", "Project Management", "PMP", "Lean Six Sigma", 
    "Technical Writing", "Public Speaking", "Team Leadership", "Conflict Resolution", "Time Management", 
    "Customer Relationship Management", "CRM", "Salesforce", "SAP", "ERP Systems", "Supply Chain Management", 
    "Digital Marketing", "SEO", "SEM", "Content Management Systems", "CMS", "WordPress", "Shopify", "Magento", 
    "Augmented Reality", "AR", "Virtual Reality", "VR", "Robotics", "ROS", "Robot Operating System", "PLC Programming", 
    "AutoCAD", "SolidWorks", "Finite Element Analysis", "FEA", "Computational Fluid Dynamics", "CFD", "Simulink", 
    "VLSI Design", "Verilog", "VHDL", "FPGA Programming", "Signal Processing", "Image Processing", "Audio Engineering", 
    "Penetration Testing Tools", "Metasploit", "Burp Suite", "Wireshark", "Nmap", "Splunk", "SIEM", "Log Analysis", 
    "Chaos Engineering", "Site Reliability Engineering", "SRE", "Monitoring Tools", "Prometheus", "Grafana", 
    "Version Control Systems", "Subversion", "SVN", "Mercurial", "Test Automation", "Selenium", "Cypress", 
    "Postman", "Unit Testing", "Integration Testing", "Performance Testing", "Load Testing", "Stress Testing", 
    "Behavior-Driven Development", "BDD", "Test-Driven Development", "TDD", "Pair Programming", "Code Review", 
    "Documentation", "API Design", "OAuth", "JWT", "Microfrontend", "Serverless Architecture", "Edge Computing", 
    "Bioinformatics", "Genomics", "Proteomics", "Molecular Modeling", "Chemoinformatics", "Financial Modeling", 
    "Risk Analysis", "Algorithm Design", "Data Structures", "Competitive Programming", "Parallel Computing", 
    "Distributed Systems", "Graph Theory", "Optimization", "Simulation", "Forecasting", "Econometrics", 
    "Geospatial Analysis", "GIS", "Geographic Information Systems", "Remote Sensing", "Satellite Imagery Analysis", 
    "Drone Technology", "Aeronautical Engineering", "Mechanical Design", "Thermodynamics", "Materials Science", 
    "Nanotechnology", "Renewable Energy Systems", "Solar Technology", "Wind Energy", "Battery Systems", 
    "Electrical Engineering", "Control Systems", "Power Electronics", "RF Engineering", "Antenna Design", 
    "Satellite Communications", "5G Technology", "Network Protocols", "TCP/IP", "DNS Management", "VPN Configuration", 
    "Customer Support", "Technical Support", "ITIL", "ServiceNow", "Help Desk Management", "Change Management", 
    "Disaster Recovery", "Business Continuity Planning", "Stakeholder Management", "Negotiation", "Critical Thinking", 
    "Problem Solving", "Emotional Intelligence", "Adaptability", "Cross-Functional Collaboration", "Mentoring", 
    "Training & Development", "Instructional Design", "E-Learning Development", "LMS", "Learning Management Systems",
    "Graphic Design", "Graphic Designer", "Developer"
]

phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp(skill.lower()) for skill in SKILLS]
phrase_matcher.add("SKILLS", patterns)


def init_db():
    conn = sqlite3.connect(AUTH_DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS companies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        company_name TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        company_description TEXT,
                        company_website TEXT,
                        company_phone TEXT,
                        company_address TEXT,
                        industry TEXT,
                        company_size TEXT,
                        founded_year TEXT,
                        contact_person_name TEXT,
                        contact_person_title TEXT,
                        linkedin_url TEXT,
                        twitter_url TEXT,
                        logo_url TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT)''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            salary TEXT NOT NULL,
            date_posted TEXT NOT NULL,
            company_id INTEGER NOT NULL,
            application_link TEXT NOT NULL,
            job_type TEXT DEFAULT 'Full-time',
            experience_level TEXT DEFAULT 'Mid-level',
            employment_type TEXT DEFAULT 'On-site',
            benefits TEXT,
            responsibilities TEXT,
            qualifications TEXT,
            deadline TEXT,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )""")
    conn.commit()
    conn.close()
    print("✓ Databases initialized successfully!")


def get_db():
    try:
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE_PATH)
            db.row_factory = sqlite3.Row
        return db
    except Exception as e:
        print("Database Connection Error:", e)
        return None


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(filepath):
    text = ""
    try:
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text("text")
        doc.close()
    except Exception as e:
        print(f"Error extracting text from PDF {filepath}: {e}")
    return text


def extract_text_from_docx(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
        
        try:
            for rel in doc.part.rels:
                if "image" in doc.part.rels[rel].target_ref:
                    image_data = doc.part.rels[rel].target_part.blob
                    image = Image.open(io.BytesIO(image_data))
                    text += pytesseract.image_to_string(image) + "\n"
        except Exception as img_error:
            print(f"Warning: Could not process images in DOCX: {img_error}")
    except Exception as e:
        print(f"Error extracting text from DOCX {filepath}: {e}")
    return text.strip()


def extract_text_from_image(filepath):
    try:
        image = Image.open(filepath)
        return pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error extracting text from image {filepath}: {e}")
        return ""


def extract_resume_text(filepath, ext):
    if ext == "pdf":
        return extract_text_from_pdf(filepath)
    elif ext == "docx":
        return extract_text_from_docx(filepath)
    elif ext in {"png", "jpg", "jpeg"}:
        return extract_text_from_image(filepath)
    return ""


def extract_skills(text):
    doc = nlp(text.lower())
    skills = set()
    
    matches = phrase_matcher(doc)
    for match_id, start, end in matches:
        skill_text = doc[start:end].text
        for original_skill in SKILLS:
            if original_skill.lower() == skill_text.lower():
                skills.add(original_skill)
                break
    
    return sorted(list(skills))


def find_jobs_from_database(skills):
    if not skills:
        return []
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE is_active = 1")
        jobs = cursor.fetchall()
        conn.close()
        
        matched_jobs = []
        user_skills_lower = [skill.lower() for skill in skills]
        
        for job in jobs:
            try:
                job_skills_raw = json.loads(job[5])
                job_skills = [skill.strip() for skill in job_skills_raw]
                job_skills_lower = [skill.lower() for skill in job_skills]
            except (json.JSONDecodeError, TypeError):
                job_skills = [skill.strip() for skill in job[5].split(",")]
                job_skills_lower = [skill.lower() for skill in job_skills]
            
            if any(user_skill in job_skills_lower for user_skill in user_skills_lower):
                matched_jobs.append({
                    "id": job[0],
                    "title": job[1],
                    "company": job[2],
                    "location": job[3],
                    "description": job[4],
                    "required_skills": job_skills,
                    "salary": job[6],
                    "date_posted": job[7],
                    "company_id": job[8],
                    "application_link": job[9],
                    "job_type": job[10],
                    "experience_level": job[11],
                    "employment_type": job[12] if len(job) > 12 else "On-site"
                })
        
        return matched_jobs
    
    except Exception as e:
        print("Database Error:", e)
        return []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search_jobs():
    skills = request.args.get("skills", "")
    
    if not skills:
        return jsonify({"job_recommendations": []})
    
    skills_list = [skill.strip() for skill in skills.split(",")]
    jobs = find_jobs_from_database(skills_list)
    
    return jsonify({"job_recommendations": jobs})


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: PDF, DOCX, PNG, JPG, JPEG"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    ext = filename.rsplit('.', 1)[1].lower()
    text = extract_resume_text(filepath, ext)
    skills = extract_skills(text)
    jobs = find_jobs_from_database(skills)

    try:
        os.remove(filepath)
    except:
        pass

    return jsonify({
        "extracted_skills": skills,
        "job_recommendations": jobs
    })


@app.route("/company/signup", methods=["GET", "POST"])
def company_signup():
    if request.method == "POST":
        company_name = request.form["company_name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        company_description = request.form.get("company_description", "").strip()
        company_website = request.form.get("company_website", "").strip()
        company_phone = request.form.get("company_phone", "").strip()
        company_address = request.form.get("company_address", "").strip()
        industry = request.form.get("industry", "").strip()
        company_size = request.form.get("company_size", "").strip()
        founded_year = request.form.get("founded_year", "").strip()
        contact_person_name = request.form.get("contact_person_name", "").strip()
        contact_person_title = request.form.get("contact_person_title", "").strip()
        
        if not company_name or not email or not password:
            flash("Company name, email, and password are required!", "danger")
            return redirect(url_for('company_signup'))
        
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('company_signup'))
        
        if len(password) < 6:
            flash("Password must be at least 6 characters long!", "danger")
            return redirect(url_for('company_signup'))
        
        hashed_password = generate_password_hash(password)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn = sqlite3.connect(AUTH_DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM companies WHERE email = ? OR company_name = ?", (email, company_name))
            existing_company = cursor.fetchone()
            
            if existing_company:
                flash("Email or company name already exists!", "danger")
                conn.close()
                return redirect(url_for('company_signup'))

            cursor.execute("""INSERT INTO companies 
                (company_name, email, password, company_description, company_website, 
                 company_phone, company_address, industry, company_size, founded_year,
                 contact_person_name, contact_person_title, created_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (company_name, email, hashed_password, company_description, company_website,
                 company_phone, company_address, industry, company_size, founded_year,
                 contact_person_name, contact_person_title, created_at))
            conn.commit()
            conn.close()

            flash("Company registration successful! Please log in.", "success")
            return redirect(url_for('company_login'))
        except sqlite3.Error as e:
            flash(f"Database error: {e}", "danger")
            return redirect(url_for('company_signup'))
    
    return render_template("company_signup.html")


@app.route("/company/login", methods=["GET", "POST"])
def company_login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        
        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return redirect(url_for('company_login'))
        
        try:
            conn = sqlite3.connect(AUTH_DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies WHERE email = ?", (email,))
            company = cursor.fetchone()
            conn.close()

            if company and check_password_hash(company[3], password):
                session["company_id"] = company[0]
                session["company_name"] = company[1]
                flash("Login successful!", "success")
                return redirect(url_for('company_dashboard'))
            else:
                flash("Invalid credentials, try again.", "danger")
        except sqlite3.Error as e:
            flash(f"Database error: {e}", "danger")
    
    return render_template("company_login.html")


@app.route('/company/logout')
def company_logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


@app.route("/company/dashboard", methods=["GET", "POST"])
def company_dashboard():
    if "company_id" not in session:
        flash("Please log in to view your dashboard.", "warning")
        return redirect(url_for("company_login"))
    
    company_id = session["company_id"]
    # Handle profile update
    if request.method == "POST":
        company_name = request.form["company_name"].strip()
        company_description = request.form.get("company_description", "").strip()
        company_website = request.form.get("company_website", "").strip()
        company_phone = request.form.get("company_phone", "").strip()
        industry = request.form.get("industry", "").strip()
        company_size = request.form.get("company_size", "").strip()
        founded_year = request.form.get("founded_year", "").strip()
        contact_person_name = request.form.get("contact_person_name", "").strip()

        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(AUTH_DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE companies 
            SET company_name = ?, company_description = ?, company_website = ?,
                company_phone = ?, industry = ?, company_size = ?, founded_year = ?,
                contact_person_name = ?, updated_at = ?
            WHERE id = ?
        """, (company_name, company_description, company_website, company_phone,
              industry, company_size, founded_year, contact_person_name, 
              updated_at, company_id))
        conn.commit()
        conn.close()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('company_dashboard'))
    
    conn = sqlite3.connect(AUTH_DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
    company_data = cursor.fetchone()
    conn.close()
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM jobs WHERE company_id = ? ORDER BY date_posted DESC", (company_id,))
    jobs_raw = cursor.fetchall()
    
    jobs = []
    for job in jobs_raw:
        try:
            skills = json.loads(job[5])
        except:
            skills = [s.strip() for s in job[5].split(",")]
        
        jobs.append({
            "id": job[0],
            "title": job[1],
            "company": job[2],
            "location": job[3],
            "description": job[4],
            "required_skills": skills,
            "salary": job[6],
            "date_posted": job[7],
            "application_link": job[9],
            "job_type": job[10],
            "experience_level": job[11],
            "employment_type": job[12] if len(job) > 12 else "On-site",
            "is_active": job[17] if len(job) > 17 else 1
        })
    
    company = {
        "id": company_data[0],
        "company_name": company_data[1],
        "email": company_data[2],
        "company_description": company_data[4],
        "company_website": company_data[5],
        "company_phone": company_data[6],
        "company_address": company_data[7],
        "industry": company_data[8],
        "company_size": company_data[9],
        "founded_year": company_data[10],
        "contact_person_name": company_data[11],
        "contact_person_title": company_data[12],
        "linkedin_url": company_data[13],
        "twitter_url": company_data[14],
        "created_at": company_data[16]
    }
    
    return render_template("company_dashboard.html", profile=company, jobs=jobs)


@app.route("/company/profile/edit", methods=["GET", "POST"])
def edit_company_profile():
    if "company_id" not in session:
        flash("Please log in to edit your profile.", "warning")
        return redirect(url_for("company_login"))
    
    company_id = session["company_id"]
    
    if request.method == "POST":
        try:
            company_name = request.form["company_name"].strip()
            company_description = request.form.get("company_description", "").strip()
            company_website = request.form.get("company_website", "").strip()
            company_phone = request.form.get("company_phone", "").strip()
            company_address = request.form.get("company_address", "").strip()
            industry = request.form.get("industry", "").strip()
            company_size = request.form.get("company_size", "").strip()
            founded_year = request.form.get("founded_year", "").strip()
            contact_person_name = request.form.get("contact_person_name", "").strip()
            contact_person_title = request.form.get("contact_person_title", "").strip()
            linkedin_url = request.form.get("linkedin_url", "").strip()
            twitter_url = request.form.get("twitter_url", "").strip()
            
            if not company_name:
                flash("Company name is required!", "danger")
                return redirect(url_for('edit_company_profile'))
            
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            conn = sqlite3.connect(AUTH_DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE companies 
                SET company_name = ?, company_description = ?, company_website = ?,
                    company_phone = ?, company_address = ?, industry = ?,
                    company_size = ?, founded_year = ?, contact_person_name = ?,
                    contact_person_title = ?, linkedin_url = ?, twitter_url = ?,
                    updated_at = ?
                WHERE id = ?
            """, (company_name, company_description, company_website, company_phone,
                  company_address, industry, company_size, founded_year,
                  contact_person_name, contact_person_title, linkedin_url, twitter_url,
                  updated_at, company_id))
            
            conn.commit()
            conn.close()
            
            session["company_name"] = company_name
            flash("Profile updated successfully!", "success")
            return redirect(url_for('company_dashboard'))
            
        except Exception as e:
            print("Error updating profile:", e)
            flash(f"Error updating profile: {str(e)}", "danger")
    
    conn = sqlite3.connect(AUTH_DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
    company_data = cursor.fetchone()
    conn.close()
    
    company = {
        "id": company_data[0],
        "company_name": company_data[1],
        "email": company_data[2],
        "company_description": company_data[4],
        "company_website": company_data[5],
        "company_phone": company_data[6],
        "company_address": company_data[7],
        "industry": company_data[8],
        "company_size": company_data[9],
        "founded_year": company_data[10],
        "contact_person_name": company_data[11],
        "contact_person_title": company_data[12],
        "linkedin_url": company_data[13],
        "twitter_url": company_data[14]
    }
    
    return render_template("edit_company_profile.html", company=company)


@app.route("/company/job/add", methods=["GET", "POST"])
def add_job():
    if "company_id" not in session:
        flash("Please log in to add a job.", "warning")
        return redirect(url_for("company_login"))

    if request.method == "POST":
        try:
            title = request.form["title"].strip()
            location = request.form["location"].strip()
            description = request.form["description"].strip()
            required_skills = request.form["required_skills"].strip()
            salary = request.form["salary"].strip()
            application_link = request.form["application_link"].strip()
            job_type = request.form.get("job_type", "Full-time").strip()
            experience_level = request.form.get("experience_level", "Mid-level").strip()
            employment_type = request.form.get("employment_type", "On-site").strip()
            benefits = request.form.get("benefits", "").strip()
            responsibilities = request.form.get("responsibilities", "").strip()
            qualifications = request.form.get("qualifications", "").strip()
            deadline = request.form.get("deadline", "").strip()
            
            if not all([title, location, description, required_skills, salary, application_link]):
                flash("All required fields must be filled!", "danger")
                return redirect(url_for('add_job'))
            
            if not application_link.startswith(('http://', 'https://')):
                flash("Application link must be a valid URL (starting with http:// or https://)", "danger")
                return redirect(url_for('add_job'))
            
            date_posted = datetime.now().strftime("%Y-%m-%d")
            company_id = session["company_id"]
            company_name = session["company_name"]

            skills_list = [skill.strip() for skill in required_skills.split(",")]
            required_skills_json = json.dumps(skills_list)

            db = get_db()
            cursor = db.cursor()

            cursor.execute("""
                INSERT INTO jobs (title, company, location, description, required_skills, salary, 
                                  date_posted, company_id, application_link, job_type, 
                                  experience_level, employment_type, benefits, responsibilities,
                                  qualifications, deadline, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (title, company_name, location, description, required_skills_json, salary, 
                  date_posted, company_id, application_link, job_type, experience_level,
                  employment_type, benefits, responsibilities, qualifications, deadline))

            db.commit()
            flash("Job posted successfully!", "success")
            return redirect(url_for('company_dashboard'))

        except Exception as e:
            print("Error:", e)
            flash(f"Error adding job: {str(e)}", "danger")
            return redirect(url_for('add_job'))

    return render_template("add_job.html")


@app.route("/company/job/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    if "company_id" not in session:
        flash("Please log in to edit jobs.", "warning")
        return redirect(url_for("company_login"))
    
    company_id = session["company_id"]
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM jobs WHERE id = ? AND company_id = ?", (job_id, company_id))
    job = cursor.fetchone()
    
    if not job:
        flash("Job not found or you don't have permission to edit it.", "danger")
        return redirect(url_for('company_dashboard'))
    
    if request.method == "POST":
        try:
            title = request.form["title"].strip()
            location = request.form["location"].strip()
            description = request.form["description"].strip()
            required_skills = request.form["required_skills"].strip()
            salary = request.form["salary"].strip()
            application_link = request.form["application_link"].strip()
            job_type = request.form.get("job_type", "Full-time").strip()
            experience_level = request.form.get("experience_level", "Mid-level").strip()
            employment_type = request.form.get("employment_type", "On-site").strip()
            benefits = request.form.get("benefits", "").strip()
            responsibilities = request.form.get("responsibilities", "").strip()
            qualifications = request.form.get("qualifications", "").strip()
            deadline = request.form.get("deadline", "").strip()
            
            if not all([title, location, description, required_skills, salary, application_link]):
                flash("All required fields must be filled!", "danger")
                return redirect(url_for('edit_job', job_id=job_id))
            
            if not application_link.startswith(('http://', 'https://')):
                flash("Application link must be a valid URL!", "danger")
                return redirect(url_for('edit_job', job_id=job_id))
            
            skills_list = [skill.strip() for skill in required_skills.split(",")]
            required_skills_json = json.dumps(skills_list)
            
            cursor.execute("""
                UPDATE jobs 
                SET title = ?, location = ?, description = ?, required_skills = ?, 
                    salary = ?, application_link = ?, job_type = ?, experience_level = ?,
                    employment_type = ?, benefits = ?, responsibilities = ?,
                    qualifications = ?, deadline = ?
                WHERE id = ? AND company_id = ?
            """, (title, location, description, required_skills_json, salary,
                  application_link, job_type, experience_level, employment_type,
                  benefits, responsibilities, qualifications, deadline, job_id, company_id))
            
            db.commit()
            flash("Job updated successfully!", "success")
            return redirect(url_for('company_dashboard'))
            
        except Exception as e:
            print("Error updating job:", e)
            flash(f"Error updating job: {str(e)}", "danger")
    
    try:
        skills = json.loads(job[5])
        skills_str = ", ".join(skills)
    except:
        skills_str = job[5]
    
    job_data = {
        "id": job[0],
        "title": job[1],
        "location": job[3],
        "description": job[4],
        "required_skills": skills_str,
        "salary": job[6],
        "application_link": job[9],
        "job_type": job[10],
        "experience_level": job[11],
        "employment_type": job[12] if len(job) > 12 else "On-site",
        "benefits": job[13] if len(job) > 13 else "",
        "responsibilities": job[14] if len(job) > 14 else "",
        "qualifications": job[15] if len(job) > 15 else "",
        "deadline": job[16] if len(job) > 16 else ""
    }
    
    return render_template("edit_job.html", job=job_data)


@app.route("/company/job/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    if "company_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    company_id = session["company_id"]
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM jobs WHERE id = ? AND company_id = ?", (job_id, company_id))
        job = cursor.fetchone()
        
        if not job:
            return jsonify({"error": "Job not found or unauthorized"}), 404
        
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        db.commit()
        
        return jsonify({"message": "Job deleted successfully"}), 200
        
    except Exception as e:
        print("Error deleting job:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/company/job/toggle/<int:job_id>", methods=["POST"])
def toggle_job_status(job_id):
    if "company_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    company_id = session["company_id"]
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT is_active FROM jobs WHERE id = ? AND company_id = ?", (job_id, company_id))
        job = cursor.fetchone()
        
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        new_status = 0 if job[0] == 1 else 1
        cursor.execute("UPDATE jobs SET is_active = ? WHERE id = ?", (new_status, job_id))
        db.commit()
        
        status_text = "active" if new_status == 1 else "inactive"
        return jsonify({"message": f"Job marked as {status_text}", "is_active": new_status}), 200
        
    except Exception as e:
        print("Error toggling job status:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    init_db()
    print("\n" + "="*60)
    print("🚀 Starting Job Viewers Application...")
    print("="*60)
    print("📍 Access at: http://localhost:5000")
    print("🏢 Company Portal: http://localhost:5000/company/login")
    print("📝 Company Signup: http://localhost:5000/company/signup")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)