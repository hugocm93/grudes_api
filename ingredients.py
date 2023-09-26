from common import app
from flask_openapi3 import Tag
from logger import logger
from model import AppliedIngredient, Ingredient, Session
from model.ingredient import auto_association
from recipes import del_recipe_from, del_result
from schemas import * 
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

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
