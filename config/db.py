from sqlalchemy import create_engine, MetaData
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

engine = create_engine(url="mysql+pymysql://ufood:ufood2022@ufoodb.c2ppwslmpouq.us-east-1.rds.amazonaws.com:3306/ufood", echo=True)
meta = MetaData()
conn = engine.connect()
