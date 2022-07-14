from fastapi import APIRouter
from schemas.shop import Shop
from config.db import conn
from sqlalchemy import select
from models.shop import tableShop
from models.user import tableUser
from models.owner import tableOwner
from models.menu import tableMenu

ownerRoute = APIRouter()

@ownerRoute.get("/owner/shop/{id}")
def shopOwner(id: int):
    try:
        dataOwner = conn.execute(select(tableUser.c.id,tableUser.c.name,tableUser.c.email,tableUser.c.phone,tableUser.c.isowner).select_from(tableUser).where(tableUser.c.id == id)).first()
        if dataOwner == []:
            return {"Error":"No se encontro al dueño"}
        else:
            dataShop = conn.execute(select(tableShop).select_from(tableShop.join(tableOwner,tableShop.c.owner_id == tableOwner.c.user_id)).where(tableOwner.c.user_id == id)).fetchall()
            print(dataShop)
            if dataShop == [] and dataOwner.isowner == 1:
                return {"res":{"Owner":{"user":dataOwner,"shop":"No tiene tiendas registradas"}}}
            else: 
                if dataShop == None and dataOwner.isowner == 1:
                    return {"res":{"Owner":{"user":dataOwner,"shop":"No tiene tiendas registradas"}}}
                elif dataShop == [] or dataOwner == 0:
                    return {"Error":"No es dueño"}
                else:
                    return {"res":{"Owner":{"user":dataOwner,"shop":dataShop}}}
    except Exception as e:
        return {"Error":str(e)}

@ownerRoute.post("/owner/shop/create")
def createShop(shop:Shop):
    try:
        test = conn.execute(select(tableUser.c.isowner).where(tableUser.c.id == shop.owner_id)).first()
        if(test.isowner == 0):
            return {"Error":"No es un dueño"}
        else:
            create = conn.execute(tableShop.insert(), shop.dict())
            conn.execute(tableMenu.insert(), {'shop_id':str(create.lastrowid)})
        return {"Restaurant":'Creado correctamente con el id'}
    except Exception as e:
        return {"Error":str(e)}