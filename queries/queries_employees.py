from fastapi import  HTTPException, Request
from sqlmodel import Session,  select, func
from database import engine
from models import Employees
 
async def count_all_employees():
    with Session(engine) as session:
        total_count = session.exec(func.count(Employees.employeeID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Employees not found")
        return total_count

async def get_all_employees(limit: int, skip: int):
    with Session(engine) as session:
        statement = select(Employees)
        employees = session.exec(statement).all()
        if not employees:
            raise HTTPException(status_code=404, detail="Employees not found")
        return employees
    
async def get_pagination_employees(request, limit:int , skip:int):
    count = await count_all_employees()
    employees = await get_all_employees(limit, skip)
    return {
        'count': count,
        'next':  f'{request.base_url}api/employees?limit={limit}&offset={skip}' if (skip + limit) < count else None,
        'previous': f'{request.base_url}api/employees?limit={limit}&offset={skip}' if skip > 0 else None,
        'employees': employees
    }

async def get_one_employee(employeeID: int):
    with Session(engine) as session:
        statement = select(Employees).where(Employees.employeeID == employeeID)
        employee = session.exec(statement).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    
async def create_employee_query( employeeName:str, title: str,  city: str,  country: str,  reportsTo: int,):
    count = await count_all_employees() 
    with Session(engine) as session:
        employee = Employees(employeeID=count  + 1, employeeName=employeeName, title=title, city=city, country=country, reportsTo=reportsTo)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee
async def update_employee_query(employeeID: int, employeeName:str, title: str,  city: str,  country: str,  reportsTo: int):
    with Session(engine) as session:
        statement = select(Employees).where(Employees.employeeID == employeeID)
        employee = session.exec(statement).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee.employeeName = employeeName
        employee.employeeTitle = title
        employee.city = city
        employee.country = country
        employee.reportsTo = reportsTo
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee

async def delete_employee_by_id(employeeID: int):
    with Session(engine) as session:
        statement = select(Employees).where(Employees.employeeID == employeeID)
        employee = session.exec(statement).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        session.delete(employee)
        session.commit()
        return employee