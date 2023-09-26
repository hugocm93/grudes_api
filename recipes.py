from common import app
from flask_openapi3 import Tag
from logger import logger
from model import Recipe, AppliedIngredient, Ingredient, Session
from schemas import * 
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

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

recipe_tag = Tag(name="Receitas", description="Adição, visualização e remoção de receitas à base")

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

@app.get('/recipe/<string:uuid>', tags=[recipe_tag],
         responses={"200": RecipeViewSchema, "404": MsgSchema})
def get_recipe(path: Path):
    """Faz a busca da receita por uuid.

    Retorna uma representação da receita.
    """

    session = Session()

    recipe = session.query(Recipe).filter(Recipe.id == path.uuid).first()

    if not recipe:
        error_msg = "Receita não encontrada na base."
        return {"message": error_msg, "detail": "uuid - " + path.uuid}, 404
    else:
        return show_recipe(recipe), 200 

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
