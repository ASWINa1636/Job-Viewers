"""
Database Migration Script for Job Viewers
This script will update your existing databases or create new ones with the correct schema
"""

import sqlite3
import os
from datetime import datetime

def migrate_databases():
    print("=" * 60)
    print("Job Viewers - Database Migration")
    print("=" * 60)
    print()
    
    # Backup existing databases
    if os.path.exists("security.db"):
        backup_name = f"security_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        print(f"📦 Backing up security.db to {backup_name}")
        os.system(f"cp security.db {backup_name}")
    
    if os.path.exists("database.db"):
        backup_name = f"database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        print(f"📦 Backing up database.db to {backup_name}")
        os.system(f"cp database.db {backup_name}")
    
    print()
    print("🔧 Creating/Updating databases...")
    print()
    
    # ====== SECURITY DATABASE (Companies) ======
    conn = sqlite3.connect("security.db")
    cursor = conn.cursor()
    
    # Drop old tables if they exist
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS company_profiles")
    
    # Create companies table (replaces users)
    print("✓ Creating companies table...")
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
        updated_at TEXT
    )''')
    
    conn.commit()
    conn.close()
    print("✓ Security database updated!")
    
    # ====== JOB DATABASE ======
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Drop old jobs table
    cursor.execute("DROP TABLE IF EXISTS jobs")
    
    # Create new jobs table with all required columns
    print("✓ Creating jobs table...")
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
    print("✓ Job database updated!")
    
    print()
    print("=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print()
    print("📊 Database Summary:")
    print("  - Companies table: Ready for company registrations")
    print("  - Jobs table: Ready with all required columns")
    print()
    print("🚀 You can now run: python app.py")
    print()

if __name__ == "__main__":
    try:
        migrate_databases()
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        print("Please check the error and try again.")