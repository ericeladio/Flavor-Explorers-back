from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes.products import product
from routes.categories import categories
from routes.shippers import shippers

app = FastAPI()


@app.get('')
def welcome():
    return {
        RedirectResponse('/docs')
    }
    
app.include_router(product)   
app.include_router(categories)
app.include_router(shippers)
 
 
