import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://se:se@localhost/se")
DEBUG = True
