from typing import Any

from pydantic.main import BaseModel


class Spec(BaseModel):
    name: str
    spec: Any


class AISpec(BaseModel):
    system: str
    host: str
