from fastapi import FastAPI
from fastapi import Depends,status # Assuming you have the FastAPI class for routing
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager #Loginmanager Class
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel#Exception class
import pymysql as sql
import uvicorn
import base64
from configparser import ConfigParser

config = ConfigParser()
config.read('CONFIG.ini')
app = FastAPI()
secret = 'secret_word'
manager = LoginManager(secret,use_cookie=True,token_url='/auth/login')
manager.cookie_name = "access_token"

class User(BaseModel):
    username:str
    email:str
    password:str
    
@manager.user_loader()
def load_user(username:str):
    connectDB(f'select username,password from users where username = "{username}";')
    if len(values) == 0:
        return 'User not found'
    else: user = values[0]
    return user

@app.post("/register")
async def register(user: User):
    username = base64.b64decode(user.username).decode('utf-8')
    connectDB(f'select username from users where username = "{username}";')
    if len(values) == 0:
        connectDB(f'insert into users (username,email,password) values ("{username}","{user.email}","{user.password}");')
        return 'Usuario Creado Satisfactoriamente'
    else:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"El nombre de usuario ya existe"})

@app.post("/auth/login")
async def loginAuth(data:OAuth2PasswordRequestForm = Depends()):
    global usuario
    username = data.username
    usuario = data.username
    password = data.password
    print(username,password)
    user = load_user(username)
    if not user:
        response = RedirectResponse(url='/auth/login',status_code=status.HTTP_400_BAD_REQUEST)
        # dataout = jsonable_encoder(access_token)
        return response
    elif password != user[1]:
        response = RedirectResponse(url='/auth/login',status_code=status.HTTP_400_BAD_REQUEST)
        return response
    access_token = manager.create_access_token(data={"sub":username})
    # print('DATA:\nuser:',user[0],' \npwd:',user[1], ' \nToken',access_token)
    response = RedirectResponse(url='/home',status_code=status.HTTP_200_OK)
    manager.set_cookie(response,access_token)
    dataout = jsonable_encoder(access_token)
    print(dataout)
    return JSONResponse(dataout)

@app.get('/home')
def home(_=Depends(manager)):
    # obtain username from cookie
    

    return usuario

def connectDB(query):   
    global values
    try:
        con = (sql.connect(host = config.get('mysql','server'),user = config.get('mysql','user'), password = config.get('mysql','password') ,database = config.get('mysql','database')))
        # print(f'Conexion Ok')
        try:
            with con.cursor() as send:
                send.execute(query)
                values = send.fetchall()
            con.commit()
        finally:
            """ Cerrar conexión """
            con.close()
            # print('[OK] : Query Executed Successfully')

    except (sql.err.OperationalError, sql.err.InternalError, sql.err.ProgrammingError, sql.err.Error, sql.err.DatabaseError,sql.err.MySQLError) as e:
        print(f'[ERROR] {e}')

if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=8000, reload=True)