from fastapi import  HTTPException
from sqlmodel import Session,  select
from database import engine
from models import Products


async def get_all_products():
    with Session(engine) as session:
        statement = select(Products)
        product = session.exec(statement).all()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product