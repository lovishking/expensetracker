# Django Expense Tracker

A simple and intuitive expense tracking application built with Django. Track your daily expenses, categorize them, and get insights into your spending habits.

![Django](https://img.shields.io/badge/Django-5.1-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ⚠️ Important Notice - Python 3.14 Compatibility

**Admin Panel Issue**: If you're using Python 3.14.0, the Django admin panel has a known compatibility issue. The main web interface works perfectly! Use the main app at http://127.0.0.1:8000/ for all functionality.

**To use the admin panel**: Either downgrade to Python 3.11 or wait for Django to release a patch for Python 3.14 compatibility.

## Features

- 📊 **Expense Management**: Add, edit, and delete expenses with ease
- 🏷️ **Category Organization**: Organize expenses into customizable categories
- 💰 **Financial Insights**: View total expenses and spending by category
- 📅 **Date Tracking**: Track expenses by date
- 🎨 **Modern UI**: Clean and responsive Bootstrap 5 interface
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Screenshots

### Expense List

View all your expenses with summary statistics and category breakdowns.

### Add/Edit Expense

Simple form interface to add or update expenses.

### Categories

Manage expense categories with automatic calculation of totals.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation

### 1. Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd expense-tracker

# Or download and extract the ZIP file
```

### 2. Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account:

- Username: (choose a username)
- Email: (optional)
- Password: (choose a secure password)

### 6. Load Sample Data (Optional)

You can create sample categories through the admin panel or the web interface.

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage

### Accessing the Application

1. **Main Application**: Navigate to `http://127.0.0.1:8000/`
2. **Admin Panel**: Navigate to `http://127.0.0.1:8000/admin/`

### Managing Categories

1. Click on "Categories" in the navigation bar
2. Click "Add Category" to create a new category
3. Fill in the category name and optional description
4. Save the category

**Recommended Categories:**

- Food & Dining
- Transportation
- Utilities
- Entertainment
- Healthcare
- Shopping
- Education
- Others

### Adding Expenses

1. Click "Add Expense" from the expense list page
2. Fill in the required fields:
   - **Title**: Brief description of the expense
   - **Amount**: Cost in dollars
   - **Category**: Select from your categories
   - **Date**: When the expense occurred
   - **Description**: Optional detailed notes
3. Click "Save Expense"

### Viewing Expenses

The main page shows:

- **Summary Statistics**: Total expenses, item count, and category count
- **Expenses by Category**: Breakdown of spending by category
- **Expense List**: All expenses with details and action buttons

### Editing and Deleting

- Click the **pencil icon** to edit an expense
- Click the **trash icon** to delete an expense
- Confirm deletion when prompted

## Project Structure

```
expense-tracker/
├── expense_tracker/          # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── expenses/                # Expenses app
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── expenses/
│   │       ├── expense_list.html
│   │       ├── expense_form.html
│   │       ├── expense_confirm_delete.html
│   │       ├── category_list.html
│   │       ├── category_form.html
│   │       └── category_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py            # Admin panel configuration
│   ├── apps.py
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL patterns
│   ├── forms.py            # Form classes
│   └── tests.py            # Unit tests
├── templates/              # Global templates
│   └── base.html           # Base template
├── static/                 # Static files (CSS, JS, images)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Models

### Category Model

```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Expense Model

```python
class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## API Endpoints (URLs)

### Expense URLs

- `/` - Expense list (home page)
- `/expense/add/` - Add new expense
- `/expense/<id>/edit/` - Edit expense
- `/expense/<id>/delete/` - Delete expense

### Category URLs

- `/categories/` - Category list
- `/category/add/` - Add new category
- `/category/<id>/edit/` - Edit category
- `/category/<id>/delete/` - Delete category

### Admin

- `/admin/` - Django admin panel

## Running Tests

Run the test suite:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test expenses
```

## Development

### Making Changes to Models

After modifying models in `models.py`:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (for production)

```bash
python manage.py collectstatic
```

## Configuration

### Settings

Key settings in `expense_tracker/settings.py`:

- **SECRET_KEY**: Change this in production!
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Add your domain in production
- **DATABASES**: Configure for production database (PostgreSQL, MySQL, etc.)
- **TIME_ZONE**: Adjust to your timezone

### Environment Variables (Recommended for Production)

Create a `.env` file for sensitive settings:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
```

## Deployment

### Preparation for Production

1. **Update Settings**:

   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for secrets
   - Configure a production database

2. **Security Checklist**:

   ```bash
   python manage.py check --deploy
   ```

3. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

### Deployment Options

- **Heroku**: Easy deployment with PostgreSQL
- **PythonAnywhere**: Simple Python hosting
- **DigitalOcean**: VPS with more control
- **AWS/Google Cloud**: Scalable cloud platforms

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'django'`
**Solution**: Make sure your virtual environment is activated and Django is installed

**Issue**: Database errors
**Solution**: Run migrations: `python manage.py migrate`

**Issue**: Static files not loading
**Solution**: Run `python manage.py collectstatic` and check `STATIC_URL` setting

**Issue**: Port already in use
**Solution**: Use a different port: `python manage.py runserver 8080`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Export expenses to CSV/PDF
- [ ] Budget setting and tracking
- [ ] Expense charts and graphs
- [ ] Monthly/yearly reports
- [ ] Receipt image uploads
- [ ] Recurring expenses
- [ ] Email notifications
- [ ] REST API for mobile apps
- [ ] Dark mode theme

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## Author

Built with ❤️ using Django

## Acknowledgments

- Django Documentation
- Bootstrap 5
- Bootstrap Icons
- The Django Community

---

**Happy Expense Tracking! 💰📊**
