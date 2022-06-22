from datetime import timedelta
import json
from fastapi import Depends, FastAPI, HTTPException, status # Assuming you have the FastAPI class for routing
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi_login import LoginManager #Loginmanager Class
from fastapi.encoders import jsonable_encoder
# from jose import JWTError, jwt
from pydantic import BaseModel#Exception class
import pymysql as sql
import uvicorn
import base64
from configparser import ConfigParser

config = ConfigParser()
config.read('CONFIG.ini')
app = FastAPI()
secret = 'secret_word'
manager = LoginManager(secret,use_cookie=True,token_url='/login')
manager.cookie_name = "access_token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# global credential

class User(BaseModel):
    first_name:str
    last_name:str
    email:str
    phone:int
    password:str
    isowner:int

@manager.user_loader()
def load_user(username:str):
    """ ENVIAR TABLE DESDE FRONT PARA CHECAR SI ES CLIENTE U OWNER ,
    ANEXAR AL HEADER 'Content-Type': 'application/x-www-form-urlencoded' y enviar en body
    """
    connectDB(f'select email,password,isowner from user where email = "{username}";')
    print('esto es values',values)
    if len(values) == 0:
        return 'User not found'
    else: 
        username = values[0]
    return username

@app.post("/auth/login")
async def loginAuth(data:OAuth2PasswordRequestForm = Depends()):
    # create variable global username
    # global credential
    # credential = data.username
    username = data.username
    password = data.password
    user = load_user(username)

    if user != 'User not found':
        if password == user[1]:
            access_token = manager.create_access_token(data={"sub":username},expires=timedelta(minutes=60))
            response = RedirectResponse(url='/home',status_code=status.HTTP_200_OK)
            response.set_cookie(manager.cookie_name,access_token)
            res = {'Token':access_token, "type":user[2]}
            # return access_token
            return JSONResponse(content=jsonable_encoder(res),status_code=status.HTTP_200_OK)
        else:
            return JSONResponse("El password es incorrecto",status_code=status.HTTP_403_FORBIDDEN)
    else:
        return JSONResponse("El usuario no existe",status_code=status.HTTP_400_BAD_REQUEST)

@app.post("/register")
async def register(user: User):
    connectDB(f'select email from user where email = "{user.email}";')
    if len(values) == 0:
        connectDB(f'insert into user (first_name,last_name,email,phone,password,isowner) values ("{user.first_name}","{user.last_name}","{user.email}","{user.phone}","{user.password}","{user.isowner}");')
        return JSONResponse("Usuario registrado",status_code=status.HTTP_200_OK)
    else:
        return JSONResponse("El usuario ya existe",status_code=status.HTTP_400_BAD_REQUEST)

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, 'secret_word', algorithms=['HS256'])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = credential
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(current_user: Cliente = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



def connectDB(query):   
    global values
    try:
        con = (sql.connect(host = config.get('mysql','server'),user = config.get('mysql','user'), password = config.get('mysql','password') ,database = config.get('mysql','database')))
        try:
            with con.cursor() as send:
                send.execute(query)
                values = send.fetchall()
            con.commit()
            return send.fetchall()
        finally:
            """ Cerrar conexión """
            con.close()

    except (sql.err.OperationalError, sql.err.InternalError, sql.err.ProgrammingError, sql.err.Error, sql.err.DatabaseError,sql.err.MySQLError) as e:
        print(f'[ERROR] {e}')
        return f'[ERROR] {e}'

if __name__ == "__main__":
    uvicorn.run("auth_users:app", host="0.0.0.0", port=9000, reload=True, debug=True)