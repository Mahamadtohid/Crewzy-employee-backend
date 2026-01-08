from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from ..schemas import EmployeeCreate, EmployeeResponse
from app.core_auth import get_current_user


from ..database import get_db
from ..models import Employee
from ..schemas import EmployeeOut
from ..core_auth import get_current_user

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/")
def get_employees(
    search: str | None = Query(default=None),
    filter_by: str = Query(default="all"), 
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    query = db.query(Employee)

    if search:
        if filter_by == "name":
            query = query.filter(Employee.name.ilike(f"%{search}%"))
        elif filter_by == "role":
            query = query.filter(Employee.role.ilike(f"%{search}%"))
        else: 
            query = query.filter(
                or_(
                    Employee.name.ilike(f"%{search}%"),
                    Employee.role.ilike(f"%{search}%"),
                )
            )

    total = query.count()

    offset = (page - 1) * limit
    employees = query.offset(offset).limit(limit).all()

    return {
        "data": employees,
        "total": total,
        "page": page,
        "limit": limit,
    }
    
from fastapi import Depends, HTTPException, status

@router.post("/", response_model=EmployeeResponse)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can add employees",
        )

    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


