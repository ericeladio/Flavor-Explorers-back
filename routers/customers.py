from fastapi import APIRouter , Request
from queries.queries_customers import (
    get_pagination_customers,
    get_one_customer,
    delete_customer_by_id,
    create_customer_query,
    update_customer_query
)

customers = APIRouter()


@customers.get("/api/customers")
async def get_customers(request: Request, limit: int = 10, offset: int = 0):
    return await get_pagination_customers(request, limit, offset)

@customers.get("/api/customer")
async def get_customer(customerID: str):
    return await get_one_customer(customerID)

@customers.post("/api/customer")
async def create_customer( companyName: str, contactName: str, contactTitle: str, city: str, country: str):
    return await create_customer_query(companyName, contactName, contactTitle, city, country)

@customers.put("/api/customer")
async def update_customer( customerID: int,companyName: str, contactName: str, contactTitle: str, city: str, country: str):
    return await update_customer_query(customerID, companyName, contactName, contactTitle, city, country)

@customers.delete("/api/customer")
async def delete_customer(customerID: int):
    return await delete_customer_by_id(customerID)



