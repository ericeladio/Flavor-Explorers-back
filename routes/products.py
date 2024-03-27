from fastapi import APIRouter
from querys import get_all_products

product = APIRouter()

@product.get('/api/products')
async def get_tasks():
  Products = await get_all_products()
  return Products