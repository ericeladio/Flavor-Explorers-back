from fastapi import APIRouter, Request
from querys import get_pagination_products, get_product

product = APIRouter()

@product.get('/api/products')
async def get_products( request: Request, skip: int = 0, limit: int = 15):
  products = await get_pagination_products( request, skip, limit)
  return products

@product.get('/api/product')
async def get_products( productID: int):
  product = await get_product(productID)
  return product
