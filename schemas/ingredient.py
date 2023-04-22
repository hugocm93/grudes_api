from pydantic import BaseModel
from typing import List
from model import Ingredient

class IngredientSchema(BaseModel):
    """ Define como um novo ingrediente a ser inserido deve ser representado
    """
    name: str = "leite"
    substitutes: List[str] = ["leite de aveia"]

IngredientViewSchema = IngredientSchema

def show_ingredient(ingredient: Ingredient):
    """ Retorna uma representação do ingrediente seguindo o schema definido em
        IngredientViewSchema.
    """

    substitutes = []
    for substitute in ingredient.substitutes:
        substitutes.append(substitute.name)

    return {
        "nome": ingredient.name,
        "substitutos": substitutes
    }

