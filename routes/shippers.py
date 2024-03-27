from fastapi import APIRouter
from queries.queries_shippers import (
  get_all_shippers,
  get_one_shipper,
  delete_shipper_by_id,
  create_shipper_query,
  update_shipper_query
)

shippers = APIRouter()

@shippers.get("/api/shippers")
async def get_shippers():
    return await get_all_shippers()

@shippers.get("/api/shipper")
async def get_shipper(shipperID: int):
    return await get_one_shipper(shipperID)
  
@shippers.post("/api/shipper")
async def create_shipper( companyName: str):
    return await create_shipper_query(companyName)

@shippers.put("/api/shipper")
async def update_shipper( shipperID: int, companyName: str):
    return await update_shipper_query(shipperID, companyName)

@shippers.delete("/api/shipper")
async def delete_shipper( shipperID: int):
    return await delete_shipper_by_id(shipperID)



