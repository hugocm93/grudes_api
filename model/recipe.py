from model import Base, AppliedIngredient
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
import uuid

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column("name", String(140))
    ingredients = relationship("AppliedIngredient")
    instructions = Column(String(1000))

    def __init__(self,\
                 name: str,\
                 ingredients: list[AppliedIngredient],\
                 instructions: str):
        self.name = name
        self.ingredients = ingredients 
        self.instructions = instructions
