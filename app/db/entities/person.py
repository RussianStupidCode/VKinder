import sqlalchemy as sql
from sqlalchemy.orm import relation, relationship
from app.db.entities.database import Base
from app.db.entities.interest import person_to_interest

# необходима для связи между подходящими людьми
person_to_person = sql.Table(
    'person_to_person', Base.metadata,
    sql.Column('first_id', sql.Integer, sql.ForeignKey('person.id')),
    sql.Column('second_id', sql.Integer, sql.ForeignKey('person.id')),
    sql.UniqueConstraint('first_id', 'second_id')
)


class Person(Base):
    __tablename__ = 'person'

    id = sql.Column(sql.Integer, primary_key=True)
    first_name = sql.Column('first_name', sql.String)
    last_name = sql.Column('last_name', sql.String)
    age = sql.Column('age', sql.Integer)
    gender = sql.Column('gender', sql.String)
    relation_status = sql.Column('status', sql.String)
    city = sql.Column('city', sql.String)

    photos = relationship('Photo')

    interests = relationship(
        "Interest",
        secondary=person_to_interest,
        back_populates="persons")

    persons = relation(
                    'Person', secondary=person_to_person,
                    primaryjoin=person_to_person.c.first_id == id,
                    secondaryjoin=person_to_person.c.second_id == id,
                    backref="second")

    def __repr__(self):
        return "".format(self.code)