from fastapi import  HTTPException
from datetime import date
from sqlmodel import Session,  select, func
from database import engine
from models import Orders, Customers, Employees, Shippers


async def count_all_orders():
    with Session(engine) as session:
        total_count = session.exec(func.count(Orders.orderID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Orders not found")
        return total_count

async def get_all_orders( limit: int, skip: int):
    with Session(engine) as session:
        statement = select(Orders, Customers.companyName, Employees.employeeName, Shippers.companyName).join(Customers, Customers.customerID == Orders.customerID).join(Employees, Employees.employeeID == Orders.employeeID).join(Shippers, Shippers.shipperID == Orders.shipperID).limit(limit).offset(skip)
        results  = session.exec(statement).all()
        orders = [{
            **result[0].model_dump(),
            'customerCompanyName': result[1], 
            'employeeName': result[2],
            'shipperCompanyName': result[3]
            } for result in results]
        if not orders:
            raise HTTPException(status_code=404, detail="Orders not found")
        return orders

async def get_pagination_orders(request, limit: int, offset: int):
    count = await count_all_orders()
    Orders = await get_all_orders(limit, offset)

    return {
        'count': count,
        'next':  f'{request.base_url}api/orders?limit={limit}&offset={offset}' if (offset + limit) < count else None,
        'previous': f'{request.base_url}api/orders?limit={limit}&offset={offset}' if offset > 0 else None,
        'Orders': Orders
    }
    
async def get_one_order(orderID: int):
    with Session(engine) as session:
        statement = select(Orders, Customers.companyName, Employees.employeeName, Shippers.companyName).join(Customers, Customers.customerID == Orders.customerID).join(Employees, Employees.employeeID == Orders.employeeID).join(Shippers, Shippers.shipperID == Orders.shipperID).where(Orders.orderID == orderID)
        result = session.exec(statement).one()
        order = {
            **result[0].model_dump(),
            'customerCompanyName': result[1], 
            'employeeName': result[2],
            'shipperCompanyName': result[3]
            } 
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
async def create_order_query( customerID: int, employeeID: str, orderDate: date, requiredDate: date, shippedDate: date, shipperID: int, freight: float):
    count = await count_all_orders() 
    with Session(engine) as session:
        order = Orders(orderID=count  + 1, customerID=customerID, employeeID=employeeID, orderDate=orderDate, requiredDate=requiredDate, shippedDate=shippedDate, shipperID=shipperID, freight=freight)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    
async def update_order_query(orderID: int, customerID: str, employeeID: int, orderDate: date, requiredDate: date, shippedDate: date, shipperID: int, freight: float ):
    with Session(engine) as session:
        statement = select(Orders).where(Orders.orderID == orderID)
        order = session.exec(statement).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.customerID = customerID
        order.employeeID = employeeID
        order.orderDate = orderDate
        order.requiredDate = requiredDate
        order.shippedDate = shippedDate
        order.shipperID = shipperID
        order.freight = freight
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

async def delete_order_by_id(orderID: int):
    with Session(engine) as session:
        statement = select(Orders).where(Orders.orderID == orderID)
        order = session.exec(statement).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        session.delete(order)
        session.commit()
        return order