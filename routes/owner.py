from fastapi import APIRouter
from schemas.shop import Shop
from config.db import conn
from sqlalchemy import select
from models.shop import tableShop
from models.user import tableUser
from models.owner import tableOwner

ownerRoute = APIRouter()

@ownerRoute.get("/owner/shop/{id}")
def shopOwner(id: int):
    dataOwner = conn.execute(select(tableUser.c.id,tableUser.c.name,tableUser.c.lastname,tableUser.c.phone,tableUser.c.email)
    .select_from(tableUser.join(tableOwner).join(tableShop)).where(tableUser.c.id == id).filter(tableOwner.c.user_id == tableUser.c.id).filter(tableShop.c.owner_id == tableOwner.c.id)).first()
    print(dataOwner,' -none?')
    if dataOwner == []:
        return {"Error":"No se encontro al dueño"}
    else:
        dataShop = conn.execute(select(tableShop).where(tableShop.c.owner_id == id)).fetchall()
        return {"res":{"Owner":{"user":dataOwner,"shop":dataShop}}}

# ENVIAR EL ID DEL OWNER EN LA PETICION PARA CREAR EL RESTAURANTE PERTENECIENTE A ESE DUEÑO
@ownerRoute.post("/owner/shop/create")
def createShop(shop:Shop):
    conn.execute(tableShop.insert(), shop.dict())
    
    return {"Restaurant":'Creado correctamente'}
