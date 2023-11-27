from types import ModuleType
from typing import Dict

from ..classes.DynamicClassCreator import DynamicClassCreator


def get_dynamic_classes(module: ModuleType) -> Dict[str, DynamicClassCreator]:
    return dict(
        (variable, getattr(module, variable))
        for variable in dir(module)
        if getattr(module, variable) in DynamicClassCreator.created_classes
    )
