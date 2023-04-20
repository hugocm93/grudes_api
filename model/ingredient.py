from model import Base
from sqlalchemy import Column, String, TypeDecorator
from typing import List
import json

class JSONList(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return []

class Ingredient(Base):
    __tablename__ = 'ingredient'

    name = Column("pk_ingredient", String(140), primary_key=True)
    substitutes = Column(JSONList)

    def __init__(self, name: str, substitutes: list[str]):
        self.name = name
        self.substitutes = substitutes
