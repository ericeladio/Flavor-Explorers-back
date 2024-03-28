from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routers import products, categories, shippers, customers

app = FastAPI()


@app.get('')
def welcome():
    return {
        RedirectResponse('/docs')
    }
    
app.include_router(products)   
app.include_router(categories)
app.include_router(shippers)
app.include_router(customers)
 
 
