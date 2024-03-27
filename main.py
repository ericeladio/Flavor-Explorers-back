from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes.products import product

app = FastAPI()


@app.get('')
def welcome():
    return {
        RedirectResponse('/docs')
    }
    
app.include_router(product)   
 
 
