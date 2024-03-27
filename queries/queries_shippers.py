from fastapi import  HTTPException, Request
from sqlmodel import Session,  select, func
from database import engine
from models import Shippers
 
async def count_all_shippers():
    with Session(engine) as session:
        total_count = session.exec(func.count(Shippers.shipperID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Shiper not found")
        return total_count

async def get_all_shippers():
    with Session(engine) as session:
        statement = select(Shippers)
        shippers = session.exec(statement).all()
        if not shippers:
            raise HTTPException(status_code=404, detail="Shippers not found")
        return shippers
    
async def get_one_shipper(shipperID: int):
    with Session(engine) as session:
        statement = select(Shippers).where(Shippers.shipperID == shipperID)
        shipper = session.exec(statement).one()
        if not shipper:
            raise HTTPException(status_code=404, detail="Shipper not found")
        return shipper
    
async def delete_shipper_by_id(shipperID: int):
    with Session(engine) as session:
        statement = select(Shippers).where(Shippers.shipperID == shipperID)
        shipper = session.exec(statement).first()
        if not shipper:
            raise HTTPException(status_code=404, detail="Shipper not found")
        session.delete(shipper)
        session.commit()
        return shipper

async def create_shipper_query(companyName: str):
    count = await count_all_shippers() 
    with Session(engine) as session:
        shipper = Shippers(shipperID=count  + 1, companyName=companyName)
        session.add(shipper)
        session.commit()
        session.refresh(shipper)
        return shipper
    
async def update_shipper_query(shipperID: int, companyName: str):
    with Session(engine) as session:
        statement = select(Shippers).where(Shippers.shipperID == shipperID)
        shipper = session.exec(statement).first()
        if not shipper:
            raise HTTPException(status_code=404, detail="Shipper not found")
        shipper.companyName = companyName
        session.add(shipper)
        session.commit()
        session.refresh(shipper)
        return shipper