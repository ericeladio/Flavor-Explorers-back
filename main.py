from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes.products import product
from routes.categories import categories

app = FastAPI()


@app.get('')
def welcome():
    return {
        RedirectResponse('/docs')
    }
    
app.include_router(product)   
app.include_router(categories)   
 
 
