from pydantic import BaseModel


class Usuario(BaseModel):
    name:str
    lastname:str
    url_avatar: str 
    email:str
    phone:str
    password:str
    isowner:bool