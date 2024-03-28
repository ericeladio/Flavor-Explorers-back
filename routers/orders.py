from fastapi import APIRouter, Request
from datetime import date
from queries.queries_orders import (
    get_pagination_orders,
    get_one_order,
    delete_order_by_id,
    create_order_query,
    update_order_query
)

orders = APIRouter()

@orders.get("/api/orders")
async def get_orders(request: Request, limit: int = 10, offset: int = 0):
    return await get_pagination_orders(request, limit, offset)

@orders.get("/api/order")
async def get_order(orderID: int):
    return await get_one_order(orderID)

@orders.post("/api/order")
async def create_order( customerID: str, employeeID: int, orderDate: date, requiredDate: date, shippedDate: date, shipperID: int, freight: float):
    return await create_order_query( customerID, employeeID, orderDate, requiredDate, shippedDate, shipperID, freight)

@orders.put("/api/order")
async def update_order( orderID: int,customerID: str, employeeID: int, orderDate: date, requiredDate: date, shippedDate: date, shipperID: int, freight: float):
    return await update_order_query(orderID, customerID, employeeID, orderDate, requiredDate, shippedDate, shipperID, freight)

@orders.delete("/api/order")
async def delete_order(orderID: int):
    return await delete_order_by_id(orderID)



