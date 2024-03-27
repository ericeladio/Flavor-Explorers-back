from fastapi import APIRouter
from querys import (
  get_all_categories, 
  create_category, 
  delete_category,
  get_one_category,
  update_category
               
)

categories = APIRouter()

@categories.get('/api/categories')
async def get_categories( ):
  categories = await get_all_categories( )
  return categories

@categories.post('/api/category')
async def create_category( categoryName: str, description: str):
  category = await create_category(categoryName, description)
  return category

@categories.get('/api/category')
async def get_category( categoryID: int):
  category = await get_one_category(categoryID)
  return category
    
@categories.put('/api/category')
async def update_category( categoryID: int, categoryName: str, description: str):
  category = await update_category(categoryID, categoryName, description)
  return category

@categories.delete('/api/category')
async def delete_category( categoryID: int):
  category = await delete_category(categoryID)
  return category
