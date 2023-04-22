from model import Recipe
from pydantic import BaseModel
from schemas import IngredientSchema, show_applied_ingredient
from schemas.aux import MsgSchema
from typing import List

class RecipeSchema(BaseModel):
    """ Define como uma nova receita a ser inserida deve ser representada.
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

class RecipeSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será                           
        feita apenas com base no nome da receita.                                                   
    """                                                                                             
    name: str = "omelete" 

class RecipesSchema(BaseModel):
    """ Lista de receitas
    """
    recipes: list[RecipeSchema]

RecipeDelSchema = MsgSchema

def show_recipe(recipe: Recipe):
    """ Retorna uma representação da receita seguindo o schema definido em
        RecipeViewSchema.
    """
    
    return {
        "nome": recipe.name,
        "ingredientes": list(map(show_applied_ingredient, recipe.ingredients)),
        "instruções": recipe.instruction,
    }

def show_recipes(recipes: list[Recipe]):
    """ Retorna uma representação das receitas seguindo o schema definido em
        RecipeViewSchema.
    """

    return {"receitas": list(map(show_recipe, recipes))}
