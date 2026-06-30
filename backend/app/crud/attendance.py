from datetime import date as date_type
from sqlalchemy.orm import Session

from app.models.attendance import AttendanceRecord
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


def get_attendance(db: Session, record_id: int) -> AttendanceRecord | None:
    return db.query(AttendanceRecord).filter(AttendanceRecord.id == record_id).first()


def list_attendance(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    employee_id: int | None = None,
    date_from: date_type | None = None,
    date_to: date_type | None = None,
    status: str | None = None,
):
    query = db.query(AttendanceRecord)
    if employee_id:
        query = query.filter(AttendanceRecord.employee_id == employee_id)
    if date_from:
        query = query.filter(AttendanceRecord.date >= date_from)
    if date_to:
        query = query.filter(AttendanceRecord.date <= date_to)
    if status:
        query = query.filter(AttendanceRecord.status == status)
    total = query.count()
    items = query.order_by(AttendanceRecord.date.desc()).offset(skip).limit(limit).all()
    return items, total


def create_attendance(db: Session, data: AttendanceCreate) -> AttendanceRecord:
    record = AttendanceRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_attendance(db: Session, record: AttendanceRecord, data: AttendanceUpdate) -> AttendanceRecord:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


def delete_attendance(db: Session, record: AttendanceRecord) -> None:
    db.delete(record)
    db.commit()
