from sqlalchemy import create_engine, MetaData
#autocommit true
from sqlalchemy.orm import sessionmaker
engine = create_engine(url="mysql+pymysql://ufood:ufood2022@ufoodb.c2ppwslmpouq.us-east-1.rds.amazonaws.com:3306/ufood")
meta = MetaData(bind=engine)
conn = engine.connect()
Session = sessionmaker(bind=engine,autocommit=True)
session = Session()
