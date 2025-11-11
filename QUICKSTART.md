# Quick Start Guide

## Get Started in 5 Minutes!

### Step 1: Set Up Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it (PowerShell)
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 2: Install Django

```powershell
pip install -r requirements.txt
```

### Step 3: Set Up Database

```powershell
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin Account

```powershell
python manage.py createsuperuser
```

Enter your preferred username, email (optional), and password.

### Step 5: Run the Server

```powershell
python manage.py runserver
```

### Step 6: Access the Application

- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First-Time Setup

### Add Your First Category

1. Go to http://127.0.0.1:8000/categories/
2. Click "Add Category"
3. Add a category (e.g., "Food", "Transport", "Entertainment")
4. Save

### Add Your First Expense

1. Go to http://127.0.0.1:8000/
2. Click "Add Expense"
3. Fill in:
   - Title: "Lunch at cafe"
   - Amount: 15.50
   - Category: Select from dropdown
   - Date: Today's date
   - Description: Optional
4. Click "Save Expense"

## Tips

- Create multiple categories first for better organization
- Use the admin panel for bulk operations
- Date defaults to today - change it for past expenses
- All amounts should be in decimal format (e.g., 15.50)

## Need Help?

Check the main README.md file for detailed documentation!
