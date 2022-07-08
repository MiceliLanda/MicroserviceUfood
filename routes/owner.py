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
    # dataOwner = conn.execute(select(tableUser.c.id,tableUser.c.name,tableUser.c.lastname,tableUser.c.phone,tableUser.c.email)
    # .select_from(tableUser.join(tableOwner).join(tableShop)).where(tableUser.c.id == id).filter(tableOwner.c.user_id == tableUser.c.id).filter(tableShop.c.owner_id == tableOwner.c.id)).first()
    dataOwner = conn.execute(select(tableUser.c.id,tableUser.c.name,tableUser.c.email,tableUser.c.phone).select_from(tableUser).where(tableUser.c.id == id)).first()
# select u.name, s.name from user u join owner o on u.id = o.user_id join shop s on s.owner_id = o.user_id;
    if dataOwner == []:
        return {"Error":"No se encontro al dueño"}
    else:
        dataShop = conn.execute(select(tableShop).where(tableShop.c.owner_id == id)).fetchall()
        if dataShop == []:
            return {"Error":"No es dueño"}
        else: 
            return {"res":{"Owner":{"user":dataOwner,"shop":dataShop}}}

# ENVIAR EL ID DEL OWNER EN LA PETICION PARA CREAR EL RESTAURANTE PERTENECIENTE A ESE DUEÑO
@ownerRoute.post("/owner/shop/create")
def createShop(shop:Shop):
    test = conn.execute(select(tableUser.c.isowner).where(tableUser.c.id == shop.owner_id)).first()
    if(test.isowner == 0):
        return {"Error":"No es un dueño"}
    else:
        conn.execute(tableShop.insert(), shop.dict())
    return {"Restaurant":'Creado correctamente'}
