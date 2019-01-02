from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env_production import DATABASE_URL, DEBUG

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=5)
DB_Session = sessionmaker(bind=engine,)
