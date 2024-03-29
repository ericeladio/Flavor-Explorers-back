from fastapi import APIRouter
from queries.queries_order_details import (
    get_order_details,
    create_order_details_query,
    update_order_details_query,
    delete_order_details_by_id
)

order_details = APIRouter()

@order_details.get("/api/order_details")
async def get_order_details_query(orderID: int):
    return await get_order_details(orderID)

@order_details.post("/api/order_details")
async def create_order_details(orderID: int, productID: int, unitPrice: float, quantity: int, discount: float):
    return await create_order_details_query(orderID, productID, unitPrice, quantity, discount)

@order_details.put("/api/order_details")
async def update_order_details( order_details_id: int, orderID: int, productID: int, unitPrice: float, quantity: int, discount: float):
    return await update_order_details_query(order_details_id, orderID, productID, unitPrice, quantity, discount)

@order_details.delete("/api/order_details")
async def delete_order_details(order_details_id: int):
    return await delete_order_details_by_id(order_details_id)




