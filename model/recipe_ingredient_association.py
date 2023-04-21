from model import Base
from sqlalchemy import Column, String, Table, ForeignKey

recipe_ingredient_association = Table(
    "recipe_ingredient_association",
    Base.metadata,
    Column("recipe_name", String(140), ForeignKey("recipes.name")),
    Column("ingredient_name", String(140), ForeignKey("ingredients.name"))
)
