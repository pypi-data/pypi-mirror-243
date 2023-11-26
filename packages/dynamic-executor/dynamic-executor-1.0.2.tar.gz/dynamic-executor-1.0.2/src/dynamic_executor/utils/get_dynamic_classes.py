from types import ModuleType

from src.dynamic_executor.classes.DynamicClassCreator import DynamicClassCreator


def get_dynamic_classes(module: ModuleType) -> dict[str, DynamicClassCreator]:
    return dict(
        (variable, value)
        for variable in dir(module)
        if (value := getattr(module, variable)) in DynamicClassCreator.created_classes
    )
