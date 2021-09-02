from db.entities.database import Base
from db.tables import Photo, Person, Interest
import db.config
import sqlalchemy as sql
from sqlalchemy.engine import URL


def session_sqlite(db_path=db.config.SQLITE_PATH):
    engine = sql.create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return sql.orm.sessionmaker(bind=engine)


def session_sql_db(database=db.config.DATABASE):
    engine = sql.create_engine(URL(**database))
    Base.metadata.create_all(engine)
    return sql.orm.sessionmaker(bind=engine)
