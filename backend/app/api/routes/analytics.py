from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import AttendanceRecord, AttendanceStatus
from app.models.employee import Employee
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/kpis")
def kpis(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    today = date.today()
    total_employees = db.query(func.count(Employee.id)).filter(Employee.is_active == 1).scalar()

    present_today = (
        db.query(func.count(AttendanceRecord.id))
        .filter(AttendanceRecord.date == today, AttendanceRecord.status == AttendanceStatus.present)
        .scalar()
    )
    late_today = (
        db.query(func.count(AttendanceRecord.id))
        .filter(AttendanceRecord.date == today, AttendanceRecord.status == AttendanceStatus.late)
        .scalar()
    )
    absent_today = (
        db.query(func.count(AttendanceRecord.id))
        .filter(AttendanceRecord.date == today, AttendanceRecord.status == AttendanceStatus.absent)
        .scalar()
    )
    on_leave_today = (
        db.query(func.count(AttendanceRecord.id))
        .filter(AttendanceRecord.date == today, AttendanceRecord.status == AttendanceStatus.on_leave)
        .scalar()
    )

    return {
        "total_employees": total_employees or 0,
        "present_today": present_today or 0,
        "late_today": late_today or 0,
        "absent_today": absent_today or 0,
        "on_leave_today": on_leave_today or 0,
    }


@router.get("/trends")
def trends(days: int = 30, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    start_date = date.today() - timedelta(days=days)
    rows = (
        db.query(
            AttendanceRecord.date,
            AttendanceRecord.status,
            func.count(AttendanceRecord.id).label("count"),
        )
        .filter(AttendanceRecord.date >= start_date)
        .group_by(AttendanceRecord.date, AttendanceRecord.status)
        .order_by(AttendanceRecord.date)
        .all()
    )

    by_date: dict[str, dict] = {}
    for row_date, status, count in rows:
        key = row_date.isoformat()
        by_date.setdefault(key, {"date": key})
        by_date[key][status.value if hasattr(status, "value") else status] = count

    return list(by_date.values())


@router.get("/department-breakdown")
def department_breakdown(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    rows = (
        db.query(Employee.department, func.count(Employee.id))
        .filter(Employee.is_active == 1)
        .group_by(Employee.department)
        .all()
    )
    return [{"department": dept or "Unassigned", "count": count} for dept, count in rows]
