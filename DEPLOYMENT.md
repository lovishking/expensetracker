# Deployment Guide - GitHub

## 🚀 Deploy Your Django Expense Tracker to GitHub

This guide will walk you through deploying your project to GitHub step-by-step.

---

## Prerequisites

1. **Git installed** - Download from https://git-scm.com/
2. **GitHub account** - Sign up at https://github.com/

---

## Step 1: Initialize Git Repository

Open PowerShell in your project folder and run:

```powershell
# Navigate to project folder (if not already there)
cd "C:\Users\Lovish Jaiswal\Desktop\expense tracker"

# Initialize git repository
git init

# Configure your name and email (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 2: Stage All Files

```powershell
# Add all files to staging area
git add .

# Check what will be committed
git status
```

You should see all your files listed in green.

---

## Step 3: Create First Commit

```powershell
# Commit the files
git commit -m "Initial commit: Django Expense Tracker with complete documentation"
```

---

## Step 4: Create GitHub Repository

1. Go to https://github.com/
2. Click the **"+"** icon in top-right corner
3. Select **"New repository"**
4. Fill in:
   - **Repository name**: `django-expense-tracker`
   - **Description**: `A simple and intuitive expense tracking web application built with Django`
   - **Public** or **Private** (your choice)
   - **DO NOT** check "Initialize with README" (we already have one)
5. Click **"Create repository"**

---

## Step 5: Connect Local Repository to GitHub

GitHub will show you commands. Use these:

```powershell
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR-USERNAME/django-expense-tracker.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

**Note:** You may be asked to login. Use your GitHub credentials.

---

## Step 6: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed on the homepage

---

## 🔐 Important: Protect Sensitive Information

### Before Making Repository Public:

1. **Change SECRET_KEY** in `settings.py`:

```python
# expense_tracker/settings.py
# Generate a new secret key at: https://djecrety.ir/

SECRET_KEY = 'django-insecure-CHANGE-THIS-TO-NEW-KEY'
```

2. **Add environment variables** (for future):

Create a `.env` file (already in .gitignore):

```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=sqlite:///db.sqlite3
```

3. **Never commit**:
   - ❌ `db.sqlite3` (database file) - Already in .gitignore ✓
   - ❌ `__pycache__/` folders - Already in .gitignore ✓
   - ❌ `venv/` virtual environment - Already in .gitignore ✓
   - ❌ `.env` files with secrets

Your `.gitignore` file already protects these!

---

## 📝 Making Changes and Updating GitHub

After making changes to your project:

```powershell
# See what changed
git status

# Add specific file
git add filename.py

# Or add all changes
git add .

# Commit with message
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

---

## 🌟 Common Git Commands

```powershell
# Check status
git status

# View commit history
git log

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes from GitHub
git pull

# Clone repository to another computer
git clone https://github.com/YOUR-USERNAME/django-expense-tracker.git

# Remove file from git (but keep locally)
git rm --cached filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD
```

---

## 🔄 Typical Workflow

```
1. Make changes to code
   ↓
2. Test locally (python manage.py runserver)
   ↓
3. git add .
   ↓
4. git commit -m "Added new feature"
   ↓
5. git push
   ↓
6. Changes appear on GitHub
```

---

## 📖 Add Project Badges to README

Add these at the top of your README.md on GitHub:

```markdown
# Django Expense Tracker

[![GitHub stars](https://img.shields.io/github/stars/YOUR-USERNAME/django-expense-tracker)](https://github.com/YOUR-USERNAME/django-expense-tracker/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR-USERNAME/django-expense-tracker)](https://github.com/YOUR-USERNAME/django-expense-tracker/network)
[![GitHub issues](https://img.shields.io/github/issues/YOUR-USERNAME/django-expense-tracker)](https://github.com/YOUR-USERNAME/django-expense-tracker/issues)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

---

## 🌐 Optional: Deploy to Live Server

### Option 1: PythonAnywhere (Free Tier Available)

1. Sign up at https://www.pythonanywhere.com/
2. Upload code from GitHub
3. Configure web app
4. Your site is live!

### Option 2: Heroku

1. Sign up at https://heroku.com/
2. Install Heroku CLI
3. Deploy with git push heroku main

### Option 3: Railway.app

1. Connect GitHub repository
2. Automatic deployments on push
3. Free tier available

---

## ✅ Checklist Before Publishing

- [ ] All files committed to git
- [ ] SECRET_KEY changed in settings.py
- [ ] db.sqlite3 in .gitignore (already done ✓)
- [ ] venv/ in .gitignore (already done ✓)
- [ ] README.md is complete and helpful
- [ ] Tested locally and everything works
- [ ] Removed any personal/sensitive data
- [ ] Added LICENSE file (optional)

---

## 🐛 Troubleshooting

### Error: "fatal: not a git repository"

**Solution:** Run `git init` first

### Error: "failed to push some refs"

**Solution:**

```powershell
git pull origin main --allow-unrelated-histories
git push origin main
```

### Error: Authentication failed

**Solution:**

1. Use Personal Access Token instead of password
2. Generate at: GitHub → Settings → Developer settings → Personal access tokens

### Large files rejected

**Solution:**

```powershell
# Remove from git
git rm --cached large-file

# Add to .gitignore
echo "large-file" >> .gitignore

# Commit
git commit -m "Removed large file"
git push
```

---

## 📱 GitHub Desktop (Alternative to Command Line)

If you prefer a GUI:

1. Download GitHub Desktop: https://desktop.github.com/
2. Clone your repository
3. Make changes
4. Click "Commit to main"
5. Click "Push origin"

Much easier for beginners!

---

## 🎓 Learning Resources

- **GitHub Docs**: https://docs.github.com/
- **Git Tutorial**: https://git-scm.com/book/en/v2
- **Interactive Git**: https://learngitbranching.js.org/

---

## 🎉 Congratulations!

Your Django Expense Tracker is now on GitHub! Share the link with others:

```
https://github.com/YOUR-USERNAME/django-expense-tracker
```

Others can now:

- View your code
- Clone and run it locally
- Contribute with pull requests
- Report issues
- Star your repository ⭐

---

## Next Steps

1. Add screenshots to README
2. Create a demo video
3. Add more features
4. Get feedback from users
5. Consider deploying to a live server

Happy coding! 🚀
