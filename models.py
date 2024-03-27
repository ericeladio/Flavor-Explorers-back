from sqlmodel import Field, SQLModel
from typing import Optional

class Products(SQLModel, table=True):
    productID: Optional[int] = Field(default=None, primary_key=True)
    productName: str
    quantityPerUnit: str
    unitPrice: float
    discontinued: int
    categoryID : int
    img : str
    
class Categories(SQLModel, table=True):
    categoryID: Optional[int] = Field(default=None, primary_key=True )
    categoryName: str
    description: str
 