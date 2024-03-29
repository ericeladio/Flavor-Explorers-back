from fastapi import  HTTPException
from sqlmodel import Session,  select, func
from database import engine
from models import Order_Details, Products


async def count_all_order_details():
    with Session(engine) as session:
        total_count = session.exec(func.count(Order_Details.orderDetailsID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Order details not found")
        return total_count


async def get_order_details(orderID: int):
    with Session(engine) as session:
        statement = select(Order_Details, Products.productName).join(Products, Order_Details.productID == Products.productID).where(Order_Details.orderID == orderID)
        results = session.exec(statement).all()
        order_details = [ {**result[0].model_dump(), 'productName': result[1]} for result in results]
        if not order_details:
            raise HTTPException(status_code=404, detail="Order details not found")
        return order_details

async def create_order_details_query( orderID: int, productID: int, unitPrice: float, quantity: int, discount: float):
    with Session(engine) as session:
        generate_id = await count_all_order_details()
        order_detail = Order_Details( orderDetailsID=generate_id + 1, orderID=orderID, productID=productID, unitPrice=unitPrice, quantity=quantity, discount=discount)
        session.add(order_detail)
        session.commit()
        session.refresh(order_detail)
        return order_detail
    
async def update_order_details_query( orderDetailsID: int, orderID: int, productID: int, unitPrice: float, quantity: int, discount: float):
    with Session(engine) as session:
        statement = select(Order_Details).where(Order_Details.orderDetailsID == orderDetailsID)
        order_detail = session.exec(statement).first()
        if not order_detail:
            raise HTTPException(status_code=404, detail="Order detail not found")
        order_detail.orderDetailsID = orderDetailsID
        order_detail.orderID = orderID
        order_detail.productID = productID
        order_detail.unitPrice = unitPrice
        order_detail.quantity = quantity
        order_detail.discount = discount
        session.add(order_detail)
        session.commit()
        session.refresh(order_detail)
        return order_detail

async def delete_order_details_by_id(orderProductID: int):
    with Session(engine) as session:
        statement = select(Order_Details).where(Order_Details.orderDetailsID == orderProductID)
        order_detail = session.exec(statement).first()
        if not order_detail:
            raise HTTPException(status_code=404, detail="Order detail not found")
        session.delete(order_detail)
        session.commit()
        return order_detail
    