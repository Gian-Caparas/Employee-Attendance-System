from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.config import settings
from app.api.routes import auth, employees, attendance, analytics

# Create tables if they don't exist (use Alembic migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Attendance & Tardiness Management System API",
    version="1.0.0",
)

origins = [o.strip() for o in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "Employee Attendance & Tardiness Management System API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
