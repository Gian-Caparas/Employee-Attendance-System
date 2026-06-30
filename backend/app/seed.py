"""
Run this once to create tables and a default admin user + sample data.

    python -m app.seed
"""
from datetime import date, timedelta

from app.database import Base, engine, SessionLocal
from app.models.user import User, RoleEnum
from app.models.employee import Employee
from app.models.attendance import AttendanceRecord, AttendanceStatus
from app.core.security import hash_password


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@company.com").first():
            admin = User(
                full_name="System Administrator",
                email="admin@company.com",
                hashed_password=hash_password("Admin123!"),
                role=RoleEnum.admin,
            )
            db.add(admin)
            print("Created admin user: admin@company.com / Admin123!")

        if db.query(Employee).count() == 0:
            sample_employees = [
                Employee(
                    employee_code="EMP-0001",
                    full_name="Maria Santos",
                    email="maria.santos@company.com",
                    department="Engineering",
                    position="Software Engineer",
                    date_hired=date.today() - timedelta(days=400),
                ),
                Employee(
                    employee_code="EMP-0002",
                    full_name="Juan Dela Cruz",
                    email="juan.delacruz@company.com",
                    department="Sales",
                    position="Account Executive",
                    date_hired=date.today() - timedelta(days=200),
                ),
                Employee(
                    employee_code="EMP-0003",
                    full_name="Ana Reyes",
                    email="ana.reyes@company.com",
                    department="HR",
                    position="HR Specialist",
                    date_hired=date.today() - timedelta(days=600),
                ),
            ]
            db.add_all(sample_employees)
            db.commit()
            print(f"Created {len(sample_employees)} sample employees")

            # sample attendance for the last 7 days
            employees = db.query(Employee).all()
            for i in range(7):
                day = date.today() - timedelta(days=i)
                for emp in employees:
                    status = AttendanceStatus.present if i % 3 != 0 else AttendanceStatus.late
                    db.add(
                        AttendanceRecord(
                            employee_id=emp.id,
                            date=day,
                            status=status,
                            minutes_late=15 if status == AttendanceStatus.late else 0,
                            source="manual",
                        )
                    )
            print("Created 7 days of sample attendance records")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
