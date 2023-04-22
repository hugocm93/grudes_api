from model import Base
from sqlalchemy import Column, String, Float, ForeignKey

class AppliedIngredient(Base):
    __tablename__ = 'applied_ingredients'

    recipe_name = Column("recipe_name", String(140), ForeignKey("recipes.name", ondelete="CASCADE"), primary_key=True)
    name = Column("name", String(140), ForeignKey("ingredients.name", ondelete="CASCADE"), primary_key=True)
    quantity = Column("quantity", Float)
    unit = Column("unit", String(50))

    def __init__(self,
                 recipe_name: str,
                 name: str,
                 quantity: float,
                 unit: str):
        self.recipe_name = recipe_name
        self.name = name
        self.quantity = quantity
        self.unit = unit
