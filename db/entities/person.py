import sqlalchemy as sql
from sqlalchemy.orm import relation, relationship
from db.entities.database import Base
from db.entities.interest import person_to_interest

# необходима для связи между подходящими людьми
person_relationship = sql.Table(
    'person_to_person', Base.metadata,
    sql.Column('first_id', sql.Integer, sql.ForeignKey('person.id')),
    sql.Column('second_id', sql.Integer, sql.ForeignKey('person.id'))
)


class Person(Base):
    __tablename__ = 'person'

    id = sql.Column(sql.Integer, primary_key=True)
    first_name = sql.Column('first_name', sql.String)
    last_name = sql.Column('last_name', sql.String)
    age = sql.Column('age', sql.Integer)
    url = sql.Column('url', sql.String)
    gender = sql.Column('gender', sql.String)
    status = sql.Column('status', sql.String)
    city = sql.Column('city', sql.String)

    photos = relationship('Photo')

    person = relationship(
        "Interest",
        secondary=person_to_interest,
        back_populates="persons")

    other_person = relation(
                    'persons', secondary=person_relationship,
                    primaryjoin=person_relationship.c.first_id == id,
                    secondaryjoin=person_relationship.c.second_id == id,
                    backref="second")

    def __repr__(self):
        return "".format(self.code)