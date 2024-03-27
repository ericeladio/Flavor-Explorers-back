from fastapi import  HTTPException, Request
from sqlmodel import Session,  select, func
from database import engine
from models import Products, Categories

#Products
async def count_all_products():
    with Session(engine) as session:
        total_count = session.exec(func.count(Products.productID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Products not found")
        return total_count

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
  
async def get_product(productID: int):
    with Session(engine) as session:
        statement = select(Products, Categories.categoryName).join(Categories, Categories.categoryID == Products.categoryID).where(Products.productID == productID)
        results = session.exec(statement).one()
        product = {**results[0].model_dump(), 'categoryName': results[1]}
        return product

async def get_all_products_by_categoryID(categoryID: int):
    with Session(engine) as session:
        statement = select(Products).where(Products.categoryID == categoryID)
        product = session.exec(statement).all()
        if not product:
            raise HTTPException(status_code=404, detail="Products not found")
        return product
    
# Categories

async def count_all_categories():
    with Session(engine) as session:
        total_count = session.exec(func.count(Categories.categoryID)).one()[0]
        if not total_count:
            raise HTTPException(status_code=404, detail="Categories not found")
        return total_count

async def get_all_categories():
    with Session(engine) as session:
        statement = select(Categories)
        categories = session.exec(statement).all()
        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
        return categories
    
async def get_one_category(categoryID: int):
    with Session(engine) as session:
        statement = select(Categories).where(Categories.categoryID == categoryID)
        category = session.exec(statement).one()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    
async def delete_category(categoryID: int):
    with Session(engine) as session:
        statement = select(Categories).where(Categories.categoryID == categoryID)
        category = session.exec(statement).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        session.delete(category)
        session.commit()
        return category

async def create_category(categoryName: str, description: str):
    count = await count_all_categories() 
    with Session(engine) as session:
        category = Categories(categoryID=count  + 1, categoryName=categoryName, description=description)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
async def update_category(categoryID: int, categoryName: str, description: str):
    with Session(engine) as session:
        statement = select(Categories).where(Categories.categoryID == categoryID)
        category = session.exec(statement).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        category.categoryName = categoryName
        category.description = description
        session.add(category)
        session.commit()
        session.refresh(category)
        return category