from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
 
 
