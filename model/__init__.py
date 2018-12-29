from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env_production import DATABASE_URL, DEBUG

engine = create_engine(DATABASE_URL, echo=DEBUG, pool_size=5, max_overflow=13)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
