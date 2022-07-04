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

@userRoute.get("/",response_model=Usuario)
def getUsers():
    user = conn.execute(tableUser.select()).first()
    return user

@userRoute.post('/auth/login')
def loginUser(data:OAuth2PasswordRequestForm=Depends()):
    user = load_user(data.username)
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    else: 
        if bcrypt.checkpw(str(data.password).encode('utf-8'),str(user.password).encode('utf-8')):
            access_token = manager.create_access_token(data={"sub":user.email},expires=timedelta(minutes=60))
            response = RedirectResponse(url='/home',status_code=status.HTTP_200_OK)
            response.set_cookie(manager.cookie_name,access_token)
            usuario = {'name':user.name,'lastname':user.lastname,'email':user.email,'phone':user.phone,'avatar_url':user.url_avatar}
            res = {'token':access_token, "user":usuario}
            return JSONResponse(content=jsonable_encoder(res),status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

@userRoute.post('/auth/register')
def registerUser(data:Usuario):
    print(data.dict())
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