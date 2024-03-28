from fastapi import  HTTPException, Request
from sqlmodel import Session,  select, func
from database import engine
from models import Categories
 
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
    
async def delete_category_by_id(categoryID: int):
    with Session(engine) as session:
        statement = select(Categories).where(Categories.categoryID == categoryID)
        category = session.exec(statement).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        session.delete(category)
        session.commit()
        return category

async def create_category_query(categoryName: str, description: str):
    count = await count_all_categories() 
    with Session(engine) as session:
        category = Categories(categoryID=count  + 1, categoryName=categoryName, description=description)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
async def update_category_query(categoryID: int, categoryName: str, description: str):
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