from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Employee
from ..schemas import EmployeeCreate, EmployeeResponse
from ..auth import get_current_user

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=List[EmployeeResponse])
def get_employees(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Employee)
    if search:
        query = query.filter(
            (Employee.name.ilike(f"%{search}%")) |
            (Employee.role.ilike(f"%{search}%"))
        )
    return query.all()

@router.post("/", response_model=EmployeeResponse)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
