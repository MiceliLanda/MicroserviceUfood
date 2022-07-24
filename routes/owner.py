from fastapi import APIRouter
from schemas.shop import Shop, ShopUpdate
from config.db import conn
from sqlalchemy import select
from models.shop import tableShop,tableSaucer,tableReview
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
            res = conn.execute(tableMenu.insert(), {'shop_id':str(create.lastrowid)})
            
        return {"Restaurant":{"idMenu":str(res.lastrowid),"idShop":str(create.lastrowid)}}
    except Exception as e:
        return {"Error":str(e)}

@ownerRoute.put("/owner/shop/update/{id}")
def updateUser(id: int, shop: ShopUpdate):
    try:
        conn.execute(tableShop.update().where(tableShop.c.id == id).values(name=shop.name,url_shop=shop.url_shop,phone=shop.phone,address=shop.address))
        return {"message": "shop actualizada exitosamente"}
    except Exception as e:
        return {"Error":str(e)}

@ownerRoute.delete("/owner/shop/delete/{id}")
def deleteShop(id_shop: int):
    try:
        # conn.execute(tableReview.delete().where(tableReview.c.shop_id == id_shop))
        # menu_id = conn.execute(select(tableMenu.c.id).where(tableMenu.c.shop_id == id_shop)).first()[0]
        # conn.execute(tableSaucer.delete().where(tableSaucer.c.menu_id == menu_id))
        conn.execute(tableMenu.delete().where(tableMenu.c.id == id_shop))
        conn.execute(tableShop.delete().where(tableShop.c.id == id_shop))
        return {"message": "Tienda eliminada exitosamente"}
    except Exception as e:
        return {"Error":str(e)}