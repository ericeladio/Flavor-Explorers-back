from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routers import *

app = FastAPI()


@app.get('/')
def welcome():
    return {
        RedirectResponse('/docs')
    }
    
app.include_router(products)   
app.include_router(categories)
app.include_router(shippers)
app.include_router(customers)
app.include_router(employees)
app.include_router(orders)
app.include_router(order_details)
 
 
