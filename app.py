from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from logger import logger
from model import Recipe, AppliedIngredient, Ingredient, Session
from schemas import IngredientSchema, IngredientViewSchema, MsgSchema, show_ingredient
from schemas import MsgSchema
from schemas import RecipeSchema, RecipeViewSchema, show_recipe
from sqlalchemy.exc import IntegrityError

info = Info(title="Grudes API", version="1.0")
app = OpenAPI(__name__, info = info)
CORS(app)

@app.get('/', tags=[Tag(name="Documentação Swagger")])
def home():
    """Redireciona para /openapi/swagger.
    """
    return redirect('/openapi/swagger')

ingredient_tag = Tag(name="Ingredientes", description="Adição, visualização e remoção de ingredientes à base")

@app.post('/ingredient', tags=[ingredient_tag],
          responses={"200": IngredientViewSchema, "409": MsgSchema, "400": MsgSchema})
def add_ingredient(form: IngredientSchema):
    """ Adiciona novo ingrediente à base de dados.
    
    Retorna estrutura do ingrediente inserido.
    """
    logger.debug("Adicionando ingrediente {}".format(form.name));

    def log_warning(name):
        logger.warning("Erro ao adicionar ingrediente {}".format(name))

    try:
        session = Session()

        substitutes_ = []
        for s in form.substitutes:
            found = session.query(Ingredient).filter_by(name=s).first(); 
            if found is not None:
                substitutes_.append(found);
            else:
                substitutes_.append(Ingredient(s, []));

        ingredient = Ingredient(
            name = form.name,
            substitutes = substitutes_
        )

        session.add(ingredient)
        session.commit()
        logger.debug("Adicionado ingrediente {}".format(ingredient.name))
        return show_ingredient(ingredient), 200
    except IntegrityError as e:
        error_msg = "Ingrediente de mesmo nome já salvo na base. "
        detail = e.args[0]
        log_warning(form.name)
        return {"message": error_msg, "detail": detail}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar ingrediente. "
        detail = e.args[0]
        log_warning(form.name)
        return {"message": error_msg, "detail": detail}, 400

recipe_tag = Tag(name="Receitas", description="Adição, visualização e remoção de receitas à base")

@app.post('/recipe', tags=[recipe_tag],
          responses={"200": RecipeViewSchema, "409": MsgSchema, "400": MsgSchema})
def add_recipe(form: RecipeSchema):
    """ Adiciona nova receita à base de dados.
    
    Retorna estrutura da receita inserida.
    """

    logger.debug("Adicionando receita {}".format(form.name));

    def log_warning(name):
        logger.warning("Erro ao adicionar receita {}".format(name))

    try:
        session = Session()

        applied_ingredients_ = []
        for idx, form_ingredient in enumerate(form.ingredients):

            applied = session.query(AppliedIngredient).filter_by(
                recipe_name=form.name, name=form_ingredient).first(); 

            if applied is not None:
                applied_ingredients_.append(applied)
            else:
                applied_ingredients_.append(
                    AppliedIngredient(
                        form.name,
                        form_ingredient,
                        form.quantities[idx],
                        form.units[idx]
                    )
                );

        recipe = Recipe(
            name = form.name,
            ingredients = applied_ingredients_,
            instruction = form.instruction
        )

        session.add(recipe)
        session.commit()
        logger.debug("Adicionada receita {}".format(recipe.name))

        return show_recipe(recipe), 200

    except IntegrityError as e:
        error_msg = "Receita ou ingrediente de mesmo nome já salvo na base. "
        detail = e.args[0]
        log_warning(form.name)

        return {"message": error_msg, "detail": detail}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar receita. "
        detail = e.args[0]
        log_warning(form.name)

        return {"message": error_msg, "detail": detail}, 400
