from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from logger import logger
from model import Ingredient, Session
from schemas import IngredientSchema, IngredientViewSchema, MsgSchema, show_ingredient
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
    ingredient = Ingredient(
        name=form.name,
        substitutes = form.substitutes
    )
    logger.debug("Adicionando ingrediente {}".format(ingredient.name));

    def log_warning():
        logger.warning("Erro ao adicionar ingrediente {}".format(ingredient.name))

    try:
        session = Session()
        session.add(ingredient)
        session.commit()
        logger.debug("Adicionado ingrediente {}".format(ingredient.name))
        return show_ingredient(ingredient), 200
    except IntegrityError as e:
        error_msg = "Ingrediente de mesmo nome já salvo na base. "
        detail = e.args[0]
        log_warning()
        return {"message": error_msg, "detail": detail}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar ingrediente. "
        detail = e.args[0]
        log_warning()
        return {"message": error_msg, "detail": detail}, 400
