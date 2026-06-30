from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceOut
from app.crud import attendance as attendance_crud
from app.api.deps import get_current_user, require_roles

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.get("")
def list_attendance(
    skip: int = 0,
    limit: int = 50,
    employee_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    items, total = attendance_crud.list_attendance(db, skip, limit, employee_id, date_from, date_to, status)
    return {"items": [AttendanceOut.model_validate(i) for i in items], "total": total}


@router.post("", response_model=AttendanceOut)
def create_attendance(
    data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "hr", "manager")),
):
    return attendance_crud.create_attendance(db, data)


@router.put("/{record_id}", response_model=AttendanceOut)
def update_attendance(
    record_id: int,
    data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "hr", "manager")),
):
    record = attendance_crud.get_attendance(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance_crud.update_attendance(db, record, data)


@router.delete("/{record_id}")
def delete_attendance(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "hr")),
):
    record = attendance_crud.get_attendance(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    attendance_crud.delete_attendance(db, record)
    return {"detail": "Attendance record deleted"}
