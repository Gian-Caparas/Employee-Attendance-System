# Employee Attendance & Tardiness Management System
A full-stack HR platform scaffold for attendance, tardiness, leave, reporting, and analytics — based on the project SRS.

## Stack
- **Frontend:** Next.js, TypeScript, Tailwind CSS, Recharts, Lucide icons
- **Backend:** FastAPI, SQLAlchemy, JWT auth, RBAC
- **Database:** SQLite (dev) / PostgreSQL (production-ready via docker-compose)
  
## What's included
- JWT authentication with role-based access control (admin / hr / manager / employee)
- Employee directory: full CRUD, search, filter by department
- Attendance records: full CRUD, filter by employee/date/status
- Analytics endpoints: KPIs, attendance trends, department breakdown
- Dashboard UI with live charts
- Audit log model (ready to wire up to write events)
- Seed script with a working admin login and sample data

## What's stubbed / not yet built (per the SRS roadmap)
- OCR import engine (state-machine parser for scanned attendance sheets)
- Leave management workflow
- Notifications
- Full report generation/exports (PDF/Excel)
- Rate limiting, full audit logging on every action

These are natural next phases — the architecture (FastAPI routers, SQLAlchemy models, Next.js pages) is already set up to extend into each of these.

## Quick start
### 1. Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.seed
uvicorn app.main:app --reload --port 8000


### 2. Frontend
cd frontend
npm install
cp .env.local.example .env.local
npm run dev

Visit **http://localhost:3000** and log in with:
- Email: admin@company.com
- Password: Admin123!
  
### 3. Or run everything with Docker
docker-compose up --build

## Folder structure
employee-attendance-system/

├── backend/

│   ├── app/

│   │   ├── models/        # SQLAlchemy ORM models

│   │   ├── schemas/       # Pydantic request/response schemas

│   │   ├── crud/          # Database operations

│   │   ├── api/routes/    # FastAPI route handlers

│   │   ├── core/          # Security (hashing, JWT)

│   │   ├── main.py        # App entry point

│   │   ├── config.py      # Settings

│   │   ├── database.py    # DB engine/session

│   │   └── seed.py        # Seed script

│   └── requirements.txt

├── frontend/

│   └── src/

│       ├── app/            # Pages (login, dashboard, employees, attendance)

│       ├── components/     # Sidebar, Header, StatCard, DataTable

│       ├── lib/             # API client, auth helpers

│       └── types/          # Shared TypeScript types

└── docker-compose.yml
