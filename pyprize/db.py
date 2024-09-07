from sqlmodel import SQLModel, create_engine
from pyprize import settings

sqlite_url = f"sqlite:///{settings.DB_NAME}"
engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
