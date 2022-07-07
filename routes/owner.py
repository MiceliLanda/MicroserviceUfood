from fastapi import APIRouter
from schemas.shop import Shop
from config.db import conn
from sqlalchemy import select
from models.shop import tableShop
from models.user import tableUser
from models.owner import tableOwner

ownerRoute = APIRouter()

@ownerRoute.get("/owner/shop")
def getShop():
    # conn.execute(select(tableUser.c.id,tableUser.c.name,tableUser.c.lastname,tableUser.c.url_avatar,tableUser.c.email,tableUser.c.phone,tableUser.c.isowner,tableOwner).select_from(tableUser.join(tableOwner, tableUser.c.id == tableOwner.c.user_id))).fetchall()
    query = conn.execute(
        select(tableUser.c.id,tableUser.c.name,tableUser.c.lastname,tableShop.c.name,tableShop.c.address)
        .select_from(tableShop
        .join(tableOwner,tableShop.c.owner_id == tableOwner.c.id)
        .join(tableUser,tableUser.c.id == tableOwner.c.user_id))).fetchall()
    # return { "Shops": conn.execute(tableShop.select()).fetchall() }
    return {"Owner":query}

# ENVIAR EL ID DEL OWNER EN LA PETICION PARA CREAR EL RESTAURANTE PERTENECIENTE A ESE DUEÑO
@ownerRoute.post("/owner/shop/create")
def createShop(shop:Shop):
    conn.execute(tableShop.insert(), shop.dict())
    return {"Restaurant":'Creado correctamente'}
