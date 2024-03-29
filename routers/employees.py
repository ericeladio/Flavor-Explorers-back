from fastapi import APIRouter, Request
from queries.queries_employees import (
    get_pagination_employees,
    get_one_employee,
    delete_employee_by_id,
    create_employee_query,
    update_employee_query
)

employees = APIRouter()

@employees.get("/api/employees")
async def get_employees(request: Request, limit: int = 10, offset: int = 0):
    return await get_pagination_employees(request, limit, offset)

@employees.get("/api/employee")
async def get_employee(employeeID: int):
    return await get_one_employee(employeeID)

@employees.post("/api/employee")
async def create_employee( employeeName:str, employeeTitle: str,  city: str,  country: str,  reportsTo: int,):
    return await create_employee_query( employeeName, employeeTitle,  city,  country,  reportsTo)

@employees.put("/api/employee")
async def update_employee( employeeID: int,employeeName:str, employeeTitle: str,  city: str,  country: str,  reportsTo: int):
    return await update_employee_query(employeeID, employeeName, employeeTitle,  city,  country,  reportsTo)

@employees.delete("/api/employee")
async def delete_employee(employeeID: int):
    return await delete_employee_by_id(employeeID)




