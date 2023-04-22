from model import Base, AppliedIngredient
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Recipe(Base):
    __tablename__ = 'recipes'

    name = Column("name", String(140), primary_key=True)
    ingredients = relationship("AppliedIngredient")
    instruction = Column(String(1000))

    def __init__(self,\
                 name: str,\
                 ingredients: list[AppliedIngredient],\
                 instruction: str):
        self.name = name
        self.ingredients = ingredients 
        self.instruction = instruction
