from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def list_employees(
    db: Session, skip: int = 0, limit: int = 50, search: str | None = None, department: str | None = None
):
    query = db.query(Employee)
    if search:
        query = query.filter(
            or_(Employee.full_name.ilike(f"%{search}%"), Employee.employee_code.ilike(f"%{search}%"))
        )
    if department:
        query = query.filter(Employee.department == department)
    total = query.count()
    items = query.order_by(Employee.full_name).offset(skip).limit(limit).all()
    return items, total


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    employee = Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee: Employee, data: EmployeeUpdate) -> Employee:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee: Employee) -> None:
    db.delete(employee)
    db.commit()
