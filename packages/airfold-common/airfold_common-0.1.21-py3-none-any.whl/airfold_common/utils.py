import os
import re
from typing import Any, Iterable, Tuple, TypeVar
from uuid import uuid4

from pydantic.main import BaseModel

OBJ_ID_RE = re.compile(r"^af[0-9a-f]{32}$")


def uuid() -> str:
    return "af" + uuid4().hex


def is_uuid(obj_id: str) -> bool:
    if obj_id:
        if OBJ_ID_RE.match(obj_id):
            return True
    return False


def model_hierarchy(model) -> dict[str, Any]:
    def _model_hierarchy(model: BaseModel) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        for field in model.__fields__.values():
            if issubclass(field.type_, BaseModel):
                fields[field.name] = _model_hierarchy(field.type_)
            else:
                fields[field.name] = field.type_
        return fields

    return _model_hierarchy(model)


def config_from_env(prefix: str) -> dict[str, str]:
    return {k.lower().replace(f"{prefix.lower()}_", ""): v for k, v in os.environ.items() if k.startswith(prefix)}


def dict_from_env(schema: dict, prefix: str) -> dict:
    _prefix: str = f"{prefix}_" if prefix else ""

    def _dict_from_env(schema: dict, prefix: str = "") -> dict:
        result: dict = {}
        for key, value in schema.items():
            if isinstance(value, dict):
                v = _dict_from_env(value, prefix + key + "_")
                if v:
                    result[key] = v
            else:
                env_key: str = f"{prefix}{key}".upper()
                if env_key in os.environ:
                    result[key] = os.environ[env_key]
                elif value == dict:
                    v = config_from_env(env_key)
                    if v:
                        result[key] = v
        return result

    return _dict_from_env(schema, _prefix)


def model_from_env(model, prefix: str) -> Any:
    schema: dict = model_hierarchy(model)
    data: dict = dict_from_env(schema, prefix)

    try:
        return model(**data)
    except Exception:
        return None


T = TypeVar("T")


def grouped(iterable: Iterable[T], n=2) -> Iterable[Tuple[T, ...]]:
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), ..."""
    return zip(*[iter(iterable)] * n)
