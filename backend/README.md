# Backend - Employee Attendance & Tardiness Management System

FastAPI + SQLAlchemy backend.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m app.seed            # creates DB tables + an admin user
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

Default seeded login:
- email: admin@company.com
- password: Admin123!

## Switching to PostgreSQL
Change `DATABASE_URL` in `.env` to e.g.
`postgresql+psycopg2://user:password@localhost:5432/attendance_db`
and `pip install psycopg2-binary`.
