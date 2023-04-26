from model import Ingredient, AppliedIngredient
from pydantic import BaseModel
from schemas.aux import MsgSchema
from typing import List

class IngredientSchema(BaseModel):
    """ Define como um novo ingrediente a ser inserido deve ser representado.
    """
    name: str = "leite"
    substitutes: List[str] = ["leite de aveia"]

IngredientViewSchema = IngredientSchema

class IngredientSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será                           
        feita apenas com base no nome do ingrediente.                                                   
    """                                                                                             
    name: str = "leite" 

IngredientDelSchema = MsgSchema

def show_ingredient(ingredient: Ingredient):
    """ Retorna uma representação do ingrediente seguindo o schema definido em
        IngredientViewSchema.
    """

    substitutes = []
    for substitute in ingredient.substitutes:
        substitutes.append(substitute.name)

    return {
        "name": ingredient.name,
        "substitutes": substitutes
    }

def show_applied_ingredient(ingredient: AppliedIngredient):
    """ Retorna uma representação do ingrediente aplicado em receita.
    """
    return {
        "ingredient": ingredient.name,
        "quantity": ingredient.quantity,
        "unit": ingredient.unit
    }
