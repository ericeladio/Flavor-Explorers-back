from fastapi import  HTTPException, Request
from sqlmodel import Session,  select, func
from database import engine
from models import Customers
 
async def count_all_customers():
    with Session(engine) as session:
        total_count = session.exec(func.count(Customers.customerID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Customer not found")
        return total_count

async def get_all_customers( limit: int, skip: int ):
    with Session(engine) as session:
        statement = select(Customers).limit(limit).offset(skip)
        customers = session.exec(statement).all()
        if not customers:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customers
    
async def get_pagination_customers(request: Request, limit: int, offset: int):
    count = await count_all_customers()
    Customers = await get_all_customers(limit, offset)

    return {
        'count': count,
        'next':  f'{request.base_url}api/customers?limit={limit}&offset={offset}' if (offset + limit) < count else None,
        'previous': f'{request.base_url}api/customers?limit={limit}&offset={offset}' if offset > 0 else None,
        'Customers': Customers
    }
    
async def get_one_customer(customerID: str):
    with Session(engine) as session:
        statement = select(Customers).where(Customers.customerID == customerID)
        customer = session.exec(statement).one()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

async def create_customer_query( companyName:str, contactName: str, contactTitle: str,  city: str, country: str):
    count = await count_all_customers() 
    with Session(engine) as session:
        customer = Customers(customerID=count  + 1, companyName=companyName, contactName=contactName, contactTitle=contactTitle, city=city, country=country)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

async def update_customer_query(customerID: int, companyName:str, contactName: str, contactTitle: str,  city: str, country: str ):
    with Session(engine) as session:
        statement = select(Customers).where(Customers.customerID == customerID)
        customer = session.exec(statement).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        customer.companyName = companyName
        customer.contactName = contactName
        customer.contactTitle = contactTitle
        customer.country = country
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

async def delete_customer_by_id(customerID: int):
    with Session(engine) as session:
        statement = select(Customers).where(Customers.customerID == customerID)
        customer = session.exec(statement).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        session.delete(customer)
        session.commit()
        return customer