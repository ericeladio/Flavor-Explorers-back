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
    
class Shippers(SQLModel, table=True):
    shipperID: Optional[int] = Field(default=None, primary_key=True )
    companyName: str

class Customers(SQLModel, table=True):
    customerID: Optional[str] = Field(default=None, primary_key=True )
    companyName: str
    contactName: str
    contactTitle: str
    city: str
    country: str

class Employees(SQLModel, table=True):
    employeeID: Optional[int] = Field(default=None, primary_key=True )
    employeeName: str
    title: str
    city: str
    country: str
    reportsTo: int
  
class Orders(SQLModel, table=True):
    orderID: Optional[int] = Field(default=None, primary_key=True )
    customerID: str
    employeeID: int
    orderDate: str
    requiredDate: str
    shippedDate: str
    shipperID: int
    freight: float
    
class OrderDetails(SQLModel, table=True):
    orderID: Optional[int] = Field(default=None, primary_key=True )
    productID: int
    unitPrice: float
    quantity: int
    discount: float
 