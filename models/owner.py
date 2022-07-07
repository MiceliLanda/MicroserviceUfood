from sqlalchemy import Table
from config.db import meta, engine

tableOwner = Table('owner', meta, autoload=True, autoload_with=engine)