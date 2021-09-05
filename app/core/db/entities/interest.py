import sqlalchemy as sql
from sqlalchemy.orm import relationship
from app.core.db.entities.database import Base

person_to_interest = sql.Table(
    'person_to_interest', Base.metadata,
    sql.Column('person_id', sql.Integer, sql.ForeignKey('person.id')),
    sql.Column('interest_id', sql.Integer, sql.ForeignKey('interest.id')),
    sql.UniqueConstraint('person_id', 'interest_id')
)


class Interest(Base):
    """Список интересов людей"""

    __tablename__ = 'interest'

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column('name', sql.String)

    persons = relationship(
        "Person",
        secondary=person_to_interest,
        back_populates="interests")

    def __repr__(self):
        return "".format(self.code)