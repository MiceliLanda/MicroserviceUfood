# import base64
# from fastapi import FastAPI,status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse,RedirectResponse
# from pydantic import BaseModel
# import pymysql as sql
# import uvicorn
# from configparser import ConfigParser
# from starlette.requests import Request
# config = ConfigParser()
# config.read('CONFIG.ini')

# # passwordHashed = base64.b64decode('bm9oYXNoZWQ=')
# # pwdPlain = passwordHashed.decode('ascii')
# # print(pwdPlain)

# app = FastAPI()

# class User(BaseModel):
#     username:str
#     email:str
#     password:str

# @app.post('/register')
# async def register(user: User):

#     username = base64.b64decode(user.username).decode('utf-8')
#     email = base64.b64decode(user.email).decode('utf-8')
#     password = base64.b64decode(user.password).decode('utf-8')
#     # print(user.username,user.email,user.password)
#     return 'Correcto'

# def connectDB(query):   
#     global values
#     try:
#         con = (sql.connect(host = config.get('mysql','server'),user = config.get('mysql','user'), password = config.get('mysql','password') ,database = config.get('mysql','database')))
#         # print(f'Conexion Ok')
#         try:
#             with con.cursor() as send:
#                 send.execute(query)
#                 values = send.fetchall()
#             con.commit()
#         finally:
#             """ Cerrar conexión """
#             con.close()
#             # print('[OK] : Query Executed Successfully')

#     except (sql.err.OperationalError, sql.err.InternalError, sql.err.ProgrammingError, sql.err.Error, sql.err.DatabaseError,sql.err.MySQLError) as e:
#         print(f'[ERROR] {e}')


# if __name__=='__main__':
#     uvicorn.run(app)

from flask import Flask,request
app = Flask(__name__)

@app.route('/login',methods=['POST'])
def hello_world():
    data = request.get_json()
    query = f'SELECT * FROM users WHERE username = "{data["username"]}" AND password = "{data["password"]}"'
    return data