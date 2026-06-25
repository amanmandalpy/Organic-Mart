# Local Development

This project runs directly with Python, Django, Bootstrap, JavaScript, REST API,
and PostgreSQL-ready settings. For beginner-friendly local work, the local
settings can use SQLite automatically when `DATABASE_URL` is not set.

## Simple Windows Run

```powershell
cd C:\Users\admin\Documents\organic
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_catalog
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Create Admin User

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## Optional Local PostgreSQL

If you want local PostgreSQL instead of SQLite, create a database and set:

```env
DATABASE_URL=postgresql://organicmart:organicmart@127.0.0.1:5432/organicmart
```

Then run:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_catalog
```

## Quality Checks

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pytest
```

## Useful Pages

- Storefront: `http://127.0.0.1:8000/`
- Products: `http://127.0.0.1:8000/products/`
- Blog: `http://127.0.0.1:8000/blog/`
- Register: `http://127.0.0.1:8000/accounts/register/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Admin: `http://127.0.0.1:8000/admin/`
