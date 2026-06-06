# HRMS

HRMS is a Django-based human resources management system for managing employees, allowances, deductions, income tax, social security, payroll, and user accounts.

## Features

- Employee profile management
- Allowance and deduction tracking
- Income tax and social security modules
- Payroll period and payroll processing support
- User authentication and account profiles
- Audit logging and history support

## Tech Stack

- Python
- Django
- SQLite for local development
- Celery and Redis dependencies for background task support
- Bootstrap 4 via Django Crispy Forms

## Project Structure

```text
HRMS/              Django project settings and root URLs
accounts/          Authentication and user profile features
allowance/         Employee allowance module
core/              Shared views, forms, and company context
deductions/        Deduction module
employee/          Employee records and related tasks
incometax/         Income tax module
payroll/           Payroll models, views, and template tags
socialsecurity/    Social security module
templates/         Django templates
static/            Static assets
media/             Local uploaded media
```

## Getting Started

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Create an admin user:

   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open the app:

   ```text
   http://127.0.0.1:8000/
   ```

## Environment And Secrets

Keep local secrets out of version control. Use a `.env` file or local settings file for values such as:

- `SECRET_KEY`
- Email usernames and passwords
- Production database credentials
- API keys

The `.gitignore` is configured to ignore common secret files and local database files.

## Database

The default development database is SQLite at `db.sqlite3`. For a fresh local setup, run migrations with:

```bash
python manage.py migrate
```

Local database files are ignored by Git so each developer can keep their own data.
