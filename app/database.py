from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv

if(load_dotenv() is None):
    load_dotenv(".env")

DATABASE_URL=os.getenv('DB_URL')


#connect 
database_engine = create_engine(DATABASE_URL)

# equivalent à un "cursor"
SessionTemplate = sessionmaker(bind=database_engine, autocommit=False, autoflush=False)

def get_cursor():
    db= SessionTemplate()
    try:
        yield db
    finally:
        db.close()