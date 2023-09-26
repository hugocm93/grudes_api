from model import Recipe
from pydantic import BaseModel, Field
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

    instructions: str = """
        Em um bowl, coloque os ovos, leite, sal, pimenta e misture.
        Aqueça uma frigideira com manteiga e azeite. 
        Despeje os ovos.
        Espere coagular e mexa com uma espátula.
        Quando o líquido estiver quase secando, dobre ou enrole a omelete e sirva.
    """

class Path(BaseModel):
    uuid: str = Field(..., description='uuid')

RecipeViewSchema = RecipeSchema

class RecipeSearchNameSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por nome.
    """                                                                                             
    name: str = "omelete"

class RecipeSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será                           
        feita com base no nome da receita e ingredientes presentes.                                                   
        Ingredientes substitutos serão considerados.
    """                                                                                             
    name: str = "";
    ingredients: list[str] = [];

class RecipesSchema(BaseModel):
    """ Lista de receitas
    """
    recipes: list[RecipeSchema]

RecipeDelSchema = MsgSchema

def show_recipe(recipe: Recipe):
    """ Retorna uma representação da receita.  """
    
    return {
        "id": recipe.id,
        "name": recipe.name,
        "ingredients": list(map(show_applied_ingredient, recipe.ingredients)),
        "instructions": recipe.instructions,
    }

def show_recipes(recipes: list[Recipe]):
    """ Retorna uma representação das receitas seguindo o schema definido em
        RecipeViewSchema.
    """

    return {"recipes": list(map(show_recipe, recipes))}
