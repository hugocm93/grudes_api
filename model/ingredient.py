from model import Base
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from typing import List

auto_association = Table('ingredient_association', Base.metadata,
    Column('ingredient_name', String(140), ForeignKey('ingredients.name'), primary_key = True),
    Column('substitute_name', String(140), ForeignKey('ingredients.name'), primary_key = True)
)

class Ingredient(Base):
    __tablename__ = "ingredients"

    name = Column("name", String(140), primary_key=True)
    substitutes = relationship("Ingredient", secondary=auto_association,
                               primaryjoin=name==auto_association.c.ingredient_name,
                               secondaryjoin=name==auto_association.c.substitute_name)

    def __init__(self, name: str, substitutes: list["Ingredient"] = []):
        self.name = name
        self.substitutes = substitutes
