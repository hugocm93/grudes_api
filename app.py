from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from logger import logger
from model import Recipe, AppliedIngredient, Ingredient, Session
from model.ingredient import auto_association
from schemas import * 
from sqlalchemy import or_, text
from sqlalchemy.exc import IntegrityError
from itertools import accumulate

info = Info(title="Grudes API", version="1.0")
app = OpenAPI(__name__, info = info)
CORS(app)

def del_recipe_from(session: Session, name: str):
    count = 0
    for recipe in session.query(Recipe).filter(Recipe.name == name).all():
        session.query(AppliedIngredient).filter(AppliedIngredient.recipe_name == recipe.name).delete()
        session.delete(recipe)
        count += 1
    return count

def del_result(logger, name:str, count: int, label: str):
    if count:
        logger.debug("Removed {} {}".format(label, name))
        return {"message": "{} removed".format(label.capitalize()), "name": name}
    error_msg = "{} not found in database.".format(name)
    logger.warning("Error removing {} {}, {}".format(label, name, error_msg))
    return {"message": error_msg}, 404

@app.get('/', tags=[Tag(name="Documentação Swagger")])
def home():
    """Redireciona para /openapi/swagger.
    """
    return redirect('/openapi/swagger')

ingredient_tag = Tag(name="Ingredientes", description="Adição, visualização e remoção de ingredientes à base")
recipe_tag = Tag(name="Receitas", description="Adição, visualização e remoção de receitas à base")

@app.post('/ingredient', tags=[ingredient_tag],
          responses={"200": IngredientViewSchema, "409": MsgSchema, "400": MsgSchema})
def add_ingredient(form: IngredientSchema):
    """ Adiciona novo ingrediente à base de dados.

    Retorna estrutura do ingrediente inserido.
    """
    form.name = form.name.strip().lower()
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

@app.get('/ingredients', tags=[ingredient_tag],
         responses={"200": IngredientsSchema, "404": MsgSchema})
def get_ingredients():
    """Faz a busca por todas os ingredientes cadastrados.

    Retorna uma representação da listagem de ingredientes.
    """
    logger.debug(f"Buscando ingredientes ")

    session = Session()

    ingredients = session.query(Ingredient).all();
    if not ingredients:
        return {"ingredients": []}, 200

    logger.debug(f"%d ingredients encontradas" % len(ingredients))
    return show_ingredients(ingredients), 200

@app.delete('/ingredient', tags=[ingredient_tag],
            responses={"200": IngredientDelSchema, "404": MsgSchema})
def del_ingredient(query: IngredientSearchSchema):
    """Deleta um ingrediente a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    logger.debug(f"Deletando dados sobre ingrediente #{query.name}")

    session = Session()

    for ingredient in session.query(AppliedIngredient).filter(AppliedIngredient.name == query.name).all():
        del_recipe_from(session, ingredient.recipe_name)

    stm = auto_association.delete().where(or_(
        getattr(auto_association.c, "ingredient_name")==query.name,
        getattr(auto_association.c, "substitute_name")==query.name))
    session.execute(stm)

    count = session.query(Ingredient).filter(Ingredient.name == query.name).delete()

    session.commit()

    return del_result(logger, query.name, count, "ingredient")

@app.post('/recipe', tags=[recipe_tag],
          responses={"200": RecipeViewSchema, "409": MsgSchema, "400": MsgSchema})
def add_recipe(form: RecipeSchema):
    """ Adiciona nova receita à base de dados.

    Retorna estrutura da receita inserida.
    """

    form.name = form.name.strip().lower()
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

        for form_ingredient in form.ingredients:
            ingredient = session.query(Ingredient).filter_by(name=form_ingredient).first();
            if ingredient is None:
                session.add(Ingredient(form_ingredient))

        recipe = Recipe(
            name = form.name,
            ingredients = applied_ingredients_,
            instructions = form.instructions
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

@app.get('/recipes', tags=[recipe_tag],
         responses={"200": RecipesSchema, "404": MsgSchema})
def get_recipes(query: RecipeSearchSchema):
    """Faz a busca por todas as receitas cadastradas usando as opções de filtragem.

    Retorna uma representação da listagem de receitas.
    """
    logger.debug(f"Buscando receitas ")

    session = Session()

    clause = ""
    if(query.name or query.ingredients):
        clause = "WHERE " 
        if query.ingredients:
            ingredients = ", ".join(map(repr, query.ingredients)) 
            clause += "(substitute_name IN ({}) OR name IN ({}))".format(ingredients, ingredients)
        if query.name:
            if clause != "WHERE ":
                clause += " AND "
            clause += "recipe_name = {}".format(repr(query.name))

    stm = text("""
        SELECT DISTINCT recipe_name
        FROM applied_ingredients LEFT OUTER JOIN ingredient_association
        ON applied_ingredients.name = ingredient_association.ingredient_name
        {}
    """.format(clause)
    )

    result = session.execute(stm).fetchall()
    names = [row["recipe_name"] for row in result]
    recipes = session.query(Recipe).filter(Recipe.name.in_(names)).all()

    if not recipes:
        return {"receitas": []}, 200
    logger.debug(f"%d receitas encontradas" % len(recipes))
    return show_recipes(recipes), 200

@app.delete('/recipe', tags=[recipe_tag],
            responses={"200": RecipeDelSchema, "404": MsgSchema})
def del_recipe(query: RecipeSearchNameSchema):
    """Deleta um receita a partir do nome informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    query.name = query.name.strip().lower()
    logger.debug(f"Deletando dados sobre receita #{query.name}")

    session = Session()
    count = del_recipe_from(session, query.name)
    session.commit()

    return del_result(logger, query.name, count, "recipe")
