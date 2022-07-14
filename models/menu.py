from sqlalchemy import Table
from config.db import meta, engine

tableMenu = Table('menu', meta, autoload=True, autoload_with=engine)