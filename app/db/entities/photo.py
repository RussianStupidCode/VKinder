import sqlalchemy as sql
from app.db.entities.database import Base


class Photo(Base):
    __tablename__ = "photo"

    id = sql.Column(sql.Integer, primary_key=True)
    url = sql.Column('url', sql.String)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey('person.id'))

