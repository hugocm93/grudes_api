from pydantic import BaseModel

class MsgSchema(BaseModel):
    """ Define apresentação de mensagem
    """
    message: str
