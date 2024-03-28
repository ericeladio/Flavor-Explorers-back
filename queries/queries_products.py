from fastapi import  HTTPException, Request
from sqlmodel import Session,  select, func
from database import engine
from models import Products, Categories

async def count_all_products():
    with Session(engine) as session:
        total_count = session.exec(func.count(Products.productID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Products not found")
        return total_count

async def count_all_products_by_categoryID(category_id: int):
    with Session(engine) as session:
        statement = (
            select(func.count(Products.productID))
            .where(Products.categoryID == category_id)
        )
        total_count = session.exec(statement).one()
        if not total_count:
            raise HTTPException(status_code=404, detail="Products not found")
        return total_count

async def verify_category_id(category_id: int):
    with Session(engine) as session:
        category = session.get(Categories, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    
async def create_product_query(productName: str, quantityPerUnit: str, unitPrice: float, discontinued: int, categoryID: int, img: str):
    count = await count_all_products()
    with Session(engine) as session:
        category = await verify_category_id(categoryID)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product = Products(
            productID=count + 1,
            productName=productName,
            quantityPerUnit=quantityPerUnit,
            unitPrice=unitPrice,
            discontinued=discontinued,
            categoryID=categoryID,
            img=img
        )
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

async def update_product_query(productID: int, productName: str, quantityPerUnit: str, unitPrice: float, discontinued: int, categoryID: int, img: str):
    with Session(engine) as session:
        product = session.get(Products, productID)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.productName = productName
        product.quantityPerUnit = quantityPerUnit
        product.unitPrice = unitPrice
        product.discontinued = discontinued
        product.categoryID = categoryID
        product.img = img
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

async def delete_product_by_id(productID: int):
    with Session(engine) as session:
        product = session.get(Products, productID)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return product

async def get_all_products(skip: int , limit: int ):
    with Session(engine) as session:
        statement = select(Products, Categories.categoryName).join(Categories, Categories.categoryID == Products.categoryID).limit(limit).offset(skip)
        results = session.exec(statement).all()
        products = [ {**result[0].model_dump(), 'categoryName': result[1]} for result in results]
        if not products:
            raise HTTPException(status_code=404, detail="Products not found")
        return products
        
async def get_pagination_products (request: Request, skip: int , limit: int ):
  count = await count_all_products()
  products = await get_all_products(skip, limit) 

  return {
    'coutn': count,
    'next:':  f'{request.base_url}api/products?skip={skip + limit}&limit={limit}' if (skip + limit) < count else None,
    'previous': f'{request.base_url}api/products?skip={skip - limit}&limit={limit}' if skip > 0 else None,
    'products': products
  }
  
async def get_one_product(productID: int):
    with Session(engine) as session:
        statement = select(Products, Categories.categoryName).join(Categories, Categories.categoryID == Products.categoryID).where(Products.productID == productID)
        results = session.exec(statement).one()
        product = {**results[0].model_dump(), 'categoryName': results[1]}
        return product

async def get_all_products_by_categoryID(categoryID: int, skip: int , limit: int ):
    with Session(engine) as session:
        statement = select(Products, Categories.categoryName).join(Categories, Categories.categoryID == Products.categoryID).where(Products.categoryID == categoryID).limit(limit).offset(skip)
        results = session.exec(statement).all()
        products = [ {**result[0].model_dump(), 'categoryName': result[1]} for result in results]
        if not products:
            raise HTTPException(status_code=404, detail="Products not found")
        return products
    
async def get_all_products_by_categoryID_pagination (request: Request, categoryID: int, skip: int , limit: int ):
  count = await count_all_products_by_categoryID(categoryID)
  products = await get_all_products_by_categoryID(categoryID, skip, limit) 

  return {
    'coutn': count,
    'next:':  f'{request.base_url}api/products?skip={skip + limit}&limit={limit}' if (skip + limit) < count else None,
    'previous': f'{request.base_url}api/products?skip={skip - limit}&limit={limit}' if skip > 0 else None,
    'products': products
  }
    
