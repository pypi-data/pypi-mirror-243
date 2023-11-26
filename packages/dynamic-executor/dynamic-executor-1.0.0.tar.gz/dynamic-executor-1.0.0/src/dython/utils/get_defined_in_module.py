from types import ModuleType
from typing import Any

from src.dython.classes.DynamicClassCreator import DynamicClassCreator


def get_defined_in_module(module: ModuleType) -> dict[str, Any]:
    return dict(
        (variable, value)
        for variable in dir(module)
        if not isinstance(value := getattr(module, variable), ModuleType)
        and not variable.startswith("__")
        and value not in DynamicClassCreator.created_classes
        and value != DynamicClassCreator
    )
