from model import Base
from sqlalchemy import Column, String, ForeignKey
from typing import List
import json
from JSONList import JSONList

class Ingredient(Base):
    __tablename__ = 'ingredients'

    name = Column("name", String(140), primary_key=True)
    substitutes = Column(JSONList)

    def __init__(self, name: str, substitutes: list[str]):
        self.name = name
        self.substitutes = substitutes
