from sqlmodel import Field, SQLModel
from typing import Optional

class Products(SQLModel, table=True):
    productID: Optional[int] = Field(default=None, primary_key=True)
    productName: str
    quantityPerUnit: str
    quantityPerUnit: float
    discontinued: int
    categoryID : int
    img : str