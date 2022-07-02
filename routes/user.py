from datetime import timedelta
import bcrypt
from fastapi import APIRouter
from models.user import tableUser
from schemas.user import Usuario
from config.db import conn
from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi_login import LoginManager
from fastapi.encoders import jsonable_encoder
from bcrypt import hashpw, gensalt

secret = 'secret_word'
manager = LoginManager(secret,use_cookie=True,token_url='/login')
manager.cookie_name = "access_token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
userRoute = APIRouter()

@userRoute.get("/users",response_model=list[Usuario])
def getUsers():
    return conn.execute(tableUser.select()).fetchall()

@userRoute.get("/user/{id}",response_model=Usuario)
def postUser(id: str):
    return conn.execute(tableUser.select().where(tableUser.c.id == id)).first()

@userRoute.delete("/user/{id}")
def deleteUser(id: str):
    result = conn.execute(tableUser.delete().where(tableUser.c.id == id))
    return 'Usuario eliminado con exito'

@userRoute.post('/add')
def createUser(userdata: Usuario):
    conn.execute(tableUser.insert(), userdata.dict())
    return 'Usuario Creado Correctamente'

@userRoute.put('/update/{id}')
def updateUser(id: str, userdata: Usuario):
    result = conn.execute(tableUser.update().where(tableUser.c.id == id).values(userdata.dict()))
    return conn.execute(tableUser.select().where(tableUser.c.id == id)).first()

@userRoute.post('/auth/login')
def loginUser(data:OAuth2PasswordRequestForm=Depends()):
    user = load_user(data.username)
    ##print('TIPO -->>>',str(user.password).encode('utf-8'),' ',str(data.password).encode('utf-8'))
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    else: 
        if bcrypt.checkpw(str(data.password).encode('utf-8'),str(user.password).encode('utf-8')):
            access_token = manager.create_access_token(data={"sub":user.email},expires=timedelta(minutes=60))
            response = RedirectResponse(url='/home',status_code=status.HTTP_200_OK)
            response.set_cookie(manager.cookie_name,access_token)
            res = {'Token':access_token, "isowner":user.isowner}
            # return access_token
            return JSONResponse(content=jsonable_encoder(res),status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

@userRoute.post('/auth/register')
def registerUser(data:Usuario):
    res = conn.execute(tableUser.select().where(tableUser.c.email == data.email)).first()
    if res == None:
        data.password = hashpw(data.password.encode('utf-8'), gensalt())
        conn.execute(tableUser.insert(), data.dict())
        return 'Usuario Creado Correctamente'
    else:
        return 'Usuario ya existe'

@manager.user_loader()
def load_user(username:str):
    return conn.execute(tableUser.select().where(tableUser.c.email == username)).first()