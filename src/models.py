from pydantic import BaseModel
from typing import List

class Attribute(BaseModel):
    name: str
    description: str
    type: str
    size: str
    modifiers: List[str]

class Table(BaseModel):
    name: str
    description: str
    notes: str
    attribute_list: List[Attribute]

class DatabaseSchema(BaseModel):
    database_name: str
    table_list: List[Table]
