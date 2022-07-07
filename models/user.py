from sqlalchemy import Table
from config.db import meta, engine

tableUser = Table('user', meta, autoload=True, autoload_with=engine)