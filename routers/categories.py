from fastapi import APIRouter
from queries.queries_categories import (
  get_all_categories, 
  create_category_query, 
  delete_category_by_id,
  get_one_category,
  update_category_query
               
)

categories = APIRouter()

@categories.get('/api/categories')
async def get_categories( ):
  categories = await get_all_categories( )
  return categories

@categories.post('/api/category')
async def create_category( categoryName: str, description: str):
  category = await create_category_query(categoryName, description)
  return category

@categories.get('/api/category')
async def get_category( categoryID: int):
  category = await get_one_category(categoryID)
  return category
    
@categories.put('/api/category')
async def update_category( categoryID: int, categoryName: str, description: str):
  category = await update_category_query(categoryID, categoryName, description)
  return category

@categories.delete('/api/category')
async def delete_category( categoryID: int):
  category = await delete_category_by_id(categoryID)
  return category
