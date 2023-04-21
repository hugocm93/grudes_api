from model import Base, Ingredient
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from JSONList import JSONList
from model import association_table

class Recipe(Base):
    __tablename__ = 'recipes'

    name = Column("name", String(140), primary_key=True)
    ingredients = relationship("Ingredient", secondary=association_table.association_table)
    quantities = Column(JSONList)
    units = Column(JSONList)
    instruction = Column(String(1000))

    def __init__(self,\
                 name: str,\
                 ingredients: list[Ingredient],\
                 quantities: list[float],\
                 units: list[str],\
                 instruction: str):
        self.name = name
        self.ingredients = ingredients 
        self.quantities = quantities
        self.units = units
        self.instruction = instruction
