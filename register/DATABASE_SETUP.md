# SQLite3 Database Setup Guide

## Overview
This project uses SQLite3 as the database for storing user registration and authentication data.

## Database Configuration

The database is already configured in `auth_project/settings.py`:

\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
\`\`\`

## Database Schema

### Users Table
The custom User model includes:
- `id` - Primary key
- `email` - Unique email address (used for login)
- `username` - Username
- `password` - Hashed password
- `avatar` - Profile picture URL (from OAuth)
- `provider` - OAuth provider name (google, github, facebook, apple)
- `provider_id` - Unique ID from OAuth provider
- `created_at` - Registration timestamp
- `updated_at` - Last update timestamp
- `is_active` - Account status
- `is_staff` - Admin access
- `is_superuser` - Superuser access

## Setup Instructions

### Option 1: Automatic Setup (Recommended)

**Linux/Mac:**
\`\`\`bash
chmod +x setup_database.sh
./setup_database.sh
\`\`\`

**Windows:**
\`\`\`bash
setup_database.bat
\`\`\`

### Option 2: Manual Setup

1. **Install dependencies:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. **Create migrations:**
\`\`\`bash
python manage.py makemigrations
\`\`\`

3. **Apply migrations to create database:**
\`\`\`bash
python manage.py migrate
\`\`\`

4. **Create superuser (optional):**
\`\`\`bash
python manage.py createsuperuser
\`\`\`

5. **Run development server:**
\`\`\`bash
python manage.py runserver
\`\`\`

## Database Location

The SQLite3 database file will be created at:
\`\`\`
project_root/db.sqlite3
\`\`\`

## Viewing Database

You can view and manage the database using:

1. **Django Admin Panel:**
   - Go to `http://localhost:8000/admin/`
   - Login with superuser credentials
   - View/edit users

2. **SQLite Browser:**
   - Download: https://sqlitebrowser.org/
   - Open `db.sqlite3` file

3. **Command Line:**
\`\`\`bash
python manage.py dbshell
\`\`\`

## Common Commands

**View all users:**
\`\`\`bash
python manage.py shell
>>> from accounts.models import User
>>> User.objects.all()
\`\`\`

**Create user programmatically:**
\`\`\`bash
python manage.py shell
>>> from accounts.models import User
>>> user = User.objects.create_user(
...     email='user@example.com',
...     username='testuser',
...     password='securepassword123'
... )
\`\`\`

**Reset database (WARNING: deletes all data):**
\`\`\`bash
rm db.sqlite3
python manage.py migrate
\`\`\`

## OAuth Provider Data Storage

When users login via OAuth providers:
- User data is automatically saved to SQLite3
- `provider` field stores the OAuth provider name
- `provider_id` stores the unique ID from that provider
- `avatar` stores the profile picture URL
- Email and username are extracted from OAuth response

## Backup

To backup your database:
\`\`\`bash
cp db.sqlite3 db.sqlite3.backup
\`\`\`

To restore:
\`\`\`bash
cp db.sqlite3.backup db.sqlite3
