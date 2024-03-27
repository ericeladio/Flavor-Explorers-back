from fastapi import APIRouter, Request
from queries.queries_products import (
  get_pagination_products, 
  get_all_products_by_categoryID_pagination, 
  get_product,
  create_product_query,
  delete_product_query,
  update_product_query
)

product = APIRouter()

@product.get('/api/products')
async def get_products( request: Request, skip: int = 0, limit: int = 15):
  products = await get_pagination_products( request, skip, limit)
  return products

@product.get('/api/products/category')
async def get_products_by_categoryID( request: Request, categoryID: int, skip: int = 0, limit: int = 15):
  products = await get_all_products_by_categoryID_pagination(request, categoryID, skip, limit)
  return products

@product.get('/api/product')
async def get_products( productID: int):
  product = await get_product(productID)
  return product

@product.post('/api/product')
async def create_product( productName: str, quantityPerUnit: str, unitPrice: float, discontinued: int, categoryID: int, img: str):
  product = await create_product_query(productName, quantityPerUnit, unitPrice, discontinued, categoryID, img)
  return product

@product.put('/api/product')
async def update_product_( productID: int, productName: str, quantityPerUnit: str, unitPrice: float, discontinued: int, categoryID: int, img: str):
  product = await update_product_query(productID, productName, quantityPerUnit, unitPrice, discontinued, categoryID, img)
  return product

@product.delete('/api/product')
async def delete_product( productID: int):
  product = await delete_product_query(productID)
  return product

