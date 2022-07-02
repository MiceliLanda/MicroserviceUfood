from fastapi import Query
from sqlalchemy import Table
from config.db import meta, conn, engine

tableUser = Table('user', meta, autoload=True, autoload_with=engine)