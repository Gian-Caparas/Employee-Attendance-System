from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.crud import employee as employee_crud
from app.api.deps import get_current_user, require_roles

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.get("")
def list_employees(
    skip: int = 0,
    limit: int = 50,
    search: str | None = None,
    department: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    items, total = employee_crud.list_employees(db, skip, limit, search, department)
    return {"items": [EmployeeOut.model_validate(i) for i in items], "total": total}


@router.post("", response_model=EmployeeOut)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "hr")),
):
    return employee_crud.create_employee(db, data)


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    emp = employee_crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "hr")),
):
    emp = employee_crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_crud.update_employee(db, emp, data)


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "hr")),
):
    emp = employee_crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee_crud.delete_employee(db, emp)
    return {"detail": "Employee deleted"}
