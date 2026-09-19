# FarmShare NZ – IT6036 Farm Equipment Sharing Web Application

A Django + MySQL assessment project implementing authentication, authorisation, server-side validation, equipment sharing, rental requests, reporting and admin management.

## Stack
Python, Django, MySQL 8 / MySQL Workbench, HTML, CSS, JavaScript, Git/GitHub, VS Code.

## Setup (Windows)
1. Install Python 3, MySQL Server + MySQL Workbench, Git and VS Code.
2. Open `database/create_database.sql` in MySQL Workbench and run it. **Change the example password** in both SQL and `.env`.
3. In VS Code terminal:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```
4. Open `http://127.0.0.1:8000/`. Admin: `http://127.0.0.1:8000/admin/`.

## GitHub evidence workflow
Create issues, assign them, develop on feature branches, make meaningful commits, open PRs, request another member's review, then merge. Each student must use their own GitHub account and preserve genuine evidence.

## Suggested issue split
- Aryan: repository/Kanban coordination + authentication/groups integration.
- Udit: equipment CRUD/search + related tests.
- [Your Full Name]: rental requests/reporting + validation/security tests + documentation.
All members review at least one important PR from another member. Adjust this split to match what your team actually does.

## Security notes
- `.env` is excluded from Git; never commit real secrets.
- Django CSRF protection is enabled and POST templates include CSRF tokens.
- Passwords use Django hashing/validators.
- ORM is used rather than concatenated SQL.
- Ownership and role checks happen server-side.
- `DEBUG=False`, HTTPS and secure cookies are required for production.

## Submission
Replace bracketed names/IDs/dates/URLs and add real screenshots. Run tests and capture evidence. Do not submit fabricated GitHub activity or peer ratings.
