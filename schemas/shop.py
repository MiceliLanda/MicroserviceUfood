from typing import Optional
from pydantic import BaseModel

class Shop(BaseModel):
    id: int
    name:str
    url_shop:str
    phone:str
    address:str
    owner_id:int

class ShopUpdate(BaseModel):
    name:str
    url_shop:str
    phone:str
    address:str
