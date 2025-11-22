# Render Deployment Guide for Expense Tracker

## Prerequisites

- GitHub repository with your code
- Render account (render.com)

## Deployment Steps

### 1. Automatic Deployment (Recommended)

1. Fork/push this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and deploy both:
   - Web service (Django app)
   - PostgreSQL database

### 2. Manual Deployment

If you prefer manual setup:

#### Database Setup

1. Create a new PostgreSQL database:
   - Name: `expense-tracker-db`
   - User: `expense_tracker_user`

#### Web Service Setup

1. Create a new Web Service
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn expense_tracker.wsgi:application`
   - **Environment Variables**:
     - `DATABASE_URL`: (auto-filled from database - DO NOT set manually)
     - `SECRET_KEY`: (generate a secure key using Render's "Generate" button)
     - `RENDER`: `true`
     - `DEBUG`: `false`
     - `ALLOWED_HOSTS`: `*`

## Environment Variables

| Variable        | Value               | Description                           |
| --------------- | ------------------- | ------------------------------------- |
| `DATABASE_URL`  | Auto-generated      | PostgreSQL connection string          |
| `SECRET_KEY`    | Generate secure key | Django secret key                     |
| `RENDER`        | `true`              | Identifies Render environment         |
| `DEBUG`         | `false`             | Disable debug in production           |
| `ALLOWED_HOSTS` | `*`                 | Allow all hosts (Render handles this) |

## Features Included

✅ **Multi-user Authentication**

- User registration and login
- Session management
- Password validation

✅ **Personal Expense Tracking**

- Add, edit, delete expenses
- Category management
- Expense filtering and search

✅ **Group Expense Sharing**

- Create and join groups
- Add shared expenses
- Automatic bill splitting
- Settlement tracking

✅ **Admin Panel**

- User management
- Group oversight
- Expense monitoring

## Post-Deployment

1. **Create Superuser**: After deployment, you may want to create a superuser for admin access:

   ```bash
   # This would need to be done via Render shell or during build
   python manage.py createsuperuser
   ```

2. **Test Features**:
   - Visit your deployed URL
   - Test user registration
   - Create test groups and expenses
   - Verify admin panel access

## Troubleshooting

### Common Issues:

1. **Static files not loading**: Ensure `STATIC_ROOT` is set correctly
2. **Database connection errors**: Check `DATABASE_URL` environment variable
3. **500 errors**: Check Render logs for detailed error messages
4. **"Scheme '://' is unknown" error**: This means `DATABASE_URL` is empty or malformed
   - For Blueprint deployment: Ensure database is created first
   - For manual deployment: Don't manually set `DATABASE_URL` - let Render auto-fill it
   - Make sure the database service is linked to your web service

### Checking Logs:

- Go to your service in Render dashboard
- Click on "Logs" tab to see real-time logs
- Look for Django error messages

## Support

If you encounter issues:

1. Check Render's documentation
2. Review Django deployment best practices
3. Check the logs for specific error messages

## Security Notes

- DEBUG is disabled in production
- HTTPS is enforced by Render
- Security headers are configured
- Database uses secure connections
