from pydantic import BaseModel

class Shop(BaseModel):
    name:str
    url_shop:str
    phone:str
    address:str
    owner_id:int