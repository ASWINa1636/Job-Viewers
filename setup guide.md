# 🚀 Complete Setup Guide - Job Viewers v3.0 (Company Edition)

## ⚠️ IMPORTANT: Database Migration Required

Your application has been completely restructured with a **company-based authentication system**. You MUST run the migration before using the app.

## Quick Setup (3 Steps)

### Step 1: Run Database Migration

```bash
python migrate_database.py
```

This will:
- Backup your old databases (if they exist)
- Create new `companies` table (replaces `users`)
- Update `jobs` table with new columns including `application_link`

### Step 2: Create Missing Templates

Run this command to create all necessary templates:

```bash
python create_templates.py
```

Or manually create the following files in the `templates/` directory:

1. **company_login.html** - Company login page
2. **company_dashboard.html** - Company dashboard with job management
3. **edit_company_profile.html** - Edit company profile

(Template code is provided below)

### Step 3: Start the Application

```bash
python app.py
```

Visit: http://localhost:5000

## What's Changed?

### 🔄 Complete System Overhaul

**OLD System:**
- Users could sign up
- Users could post jobs
- No company profiles
- Application links optional

**NEW System:**
- **Companies** register with full details
- Companies manage their profile
- Companies post/edit/delete jobs
- **Application links are REQUIRED** for all job postings
- No user/job seeker login (they just search jobs)

### 📊 New Database Structure

**Companies Table** (in security.db):
```sql
- id
- company_name (UNIQUE, REQUIRED)
- email (UNIQUE, REQUIRED)
- password (HASHED, REQUIRED)
- company_description
- company_website
- company_phone
- company_address
- industry
- company_size
- founded_year
- contact_person_name
- contact_person_title
- linkedin_url
- twitter_url
- logo_url
- created_at
- updated_at
```

**Jobs Table** (in database.db):
```sql
- id
- title
- company
- location
- description
- required_skills (JSON)
- salary
- date_posted
- company_id (FOREIGN KEY)
- application_link (REQUIRED!)
- job_type (Full-time/Part-time/etc.)
- experience_level (Entry/Mid/Senior/etc.)
- employment_type (On-site/Remote/Hybrid)
- benefits
- responsibilities
- qualifications
- deadline
- is_active (0 or 1)
```

## URL Structure

### Public (No Login Required)
- `/` - Home page (job search)
- `/search` - Search jobs API
- `/upload` - Upload resume API

### Company Portal (Login Required)
- `/company/signup` - Company registration
- `/company/login` - Company login
- `/company/logout` - Logout
- `/company/dashboard` - Main dashboard
- `/company/profile/edit` - Edit profile
- `/company/job/add` - Post new job
- `/company/job/edit/<id>` - Edit job
- `/company/job/delete/<id>` - Delete job
- `/company/job/toggle/<id>` - Activate/deactivate job

## Features

### For Companies:
✅ Comprehensive registration with company details
✅ Editable company profile
✅ Post jobs with application links (REQUIRED)
✅ Edit existing jobs
✅ Delete jobs
✅ Toggle job active/inactive status
✅ View all posted jobs in dashboard

### For Job Seekers:
✅ Search jobs by skills
✅ Upload resume for automatic skill extraction
✅ View job details including application link
✅ Click "Apply Now" button to apply directly
✅ See job type, experience level, employment type

## Application Links - IMPORTANT!

**Application links are now REQUIRED** for all job postings.

Valid formats:
- ✅ `https://company.com/careers/apply/123`
- ✅ `https://forms.google.com/job-application`
- ✅ `https://linkedin.com/jobs/apply/456`
- ❌ `company.com/apply` (missing https://)
- ❌ `www.company.com` (not a complete URL)

The system validates that links start with `http://` or `https://`

## Migration Notes

If you had existing data:
1. Old databases are backed up with timestamp
2. You'll need to re-register companies
3. You'll need to re-post jobs with application links
4. No data migration is provided (clean start)

## Template Files Needed

Create these files in `templates/` directory:

### 1. company_login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company Login - Job Viewers</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 450px;
            padding: 50px 40px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 15px;
            color: #333;
            font-size: 2.2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.95em;
        }
        .logo {
            text-align: center;
            margin-bottom: 25px;
            font-size: 4em;
        }
        .flash-messages { margin-bottom: 20px; }
        .alert {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            text-align: center;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .form-group {
            margin-bottom: 22px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .login-btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 17px;
            font-weight: 600;
            margin-top: 12px;
            transition: all 0.3s;
        }
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        .links {
            margin-top: 25px;
            text-align: center;
        }
        .links p {
            color: #666;
            margin-bottom: 10px;
        }
        .links a {
            text-decoration: none;
            color: #667eea;
            font-weight: 600;
            transition: color 0.3s;
        }
        .links a:hover {
            color: #5568d3;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🏢</div>
        <h1>Company Login</h1>
        <p class="subtitle">Access your dashboard and manage job postings</p>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <form method="POST" action="{{ url_for('company_login') }}">
            <div class="form-group">
                <label for="email">Company Email</label>
                <input type="email" id="email" name="email" placeholder="Enter company email" required autofocus>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter password" required>
            </div>
            
            <button type="submit" class="login-btn">🔐 Login</button>
        </form>
        
        <div class="links">
            <p>Don't have an account? <a href="{{ url_for('company_signup') }}">Register Company</a></p>
            <p><a href="{{ url_for('index') }}">← Back to Home</a></p>
        </div>
    </div>
</body>
</html>
```

Save this as `templates/company_login.html`

### 2. company_dashboard.html

This file is complex. Use the `company_profile.html` template you already have and rename it to `company_dashboard.html`, then update the form action URLs and page title.

### 3. edit_company_profile.html

Create a form similar to company_signup but pre-filled with existing data for editing.

## Troubleshooting

### "table jobs has no column named application_link"
✅ **Solution**: Run `python migrate_database.py`

### "Can't login"
✅ **Solution**: Old users table is replaced. Register as a company first.

### "Application link required"
✅ **This is intentional**. All jobs must have application links now.

### "Templates not found"
✅ **Solution**: Create the missing templates listed above.

## Next Steps

1. Run migration: `python migrate_database.py`
2. Start app: `python app.py`
3. Register your company at: http://localhost:5000/company/signup
4. Login and start posting jobs!

---

**Version**: 3.0 (Company Edition)
**Last Updated**: January 2026