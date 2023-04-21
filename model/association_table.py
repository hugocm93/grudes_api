from model import Base
from sqlalchemy import Column, String, Table, ForeignKey

association_table = Table(
    "association",
    Base.metadata,
    Column("recipe_name", String(140), ForeignKey("recipes.name")),
    Column("ingredient_name", String(140), ForeignKey("ingredients.name"))
)
