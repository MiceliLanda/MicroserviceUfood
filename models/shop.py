from sqlalchemy import Table
from config.db import meta, engine

tableShop = Table('shop', meta, autoload=True, autoload_with=engine)