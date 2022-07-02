from sqlalchemy import create_engine, MetaData
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

engine = create_engine(url=os.environ.get("DATABASE_URL"), echo=True)
meta = MetaData()
conn = engine.connect()
