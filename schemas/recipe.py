from model import Recipe
from pydantic import BaseModel
from schemas import IngredientSchema
from typing import List

class RecipeSchema(BaseModel):
    """ Define como uma nova receita a ser inserida deve ser representada
    """
    name: str = "omelete"
    ingredients: list[str] = ["ovo", "leite", "sal", "pimenta", "manteiga", "azeite"]
    quantities: list[float] = [3, 2, 0.5, 0.25, 3, 1]
    units: list[str] = ["unidade", "colher de sopa", "colher de chá",\
                        "colher de chá", "colher de sopa", "colher de sopa"]

    instruction: str = """
        Em um bowl, coloque os ovos, leite, sal, pimenta e misture.
        Aqueça uma frigideira com manteiga e azeite. 
        Despeje os ovos.
        Espere coagular e mexa com uma espátula.
        Quando o líquido estiver quase secando, dobre ou enrole a omelete e sirva.
    """

RecipeViewSchema = RecipeSchema

def show_recipe(recipe: Recipe):
    """ Retorna uma representação da receita seguindo o schema definido em
        RecipeViewSchema.
    """

    ingredients = []
    for ingredient in recipe.ingredients:
        ingredients.append({
            "ingrediente": ingredient.name,
            "quantidade": ingredient.quantity,
            "unidade": ingredient.unit,
        })

    return {
        "nome": recipe.name,
        "ingredientes": ingredients,
        "instruções": recipe.instruction,
    }

