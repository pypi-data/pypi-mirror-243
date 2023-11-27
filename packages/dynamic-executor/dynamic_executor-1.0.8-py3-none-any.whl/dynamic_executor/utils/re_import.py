import importlib
from inspect import getmodule
from itertools import starmap
from types import ModuleType
from typing import Callable, Dict, Any, Optional, Tuple

from .get_dynamic_classes import get_dynamic_classes
from ..classes.DynamicClassCreator import DynamicClassCreator


def re_import_dynamic_classes(
    module_name: str, dynamic_classes: Dict[str, Dict[str, DynamicClassCreator]]
) -> ModuleType:
    re_imported_module = importlib.import_module(module_name)
    for variable, dynamic_class in dynamic_classes[module_name].items():
        new_class = getattr(re_imported_module, variable)
        for instance in dynamic_class._instances:
            instance.__class__ = new_class
        new_class._instances = dynamic_class._instances
    return re_imported_module


def get_module_variable(module: ModuleType, __locals: Dict, variable: str) -> str:
    if hasattr(module, variable):
        return variable
    return next(
        var for var in dir(module) if __locals[variable] == getattr(module, var)
    )


def re_import_modules(modules: Dict[str, ModuleType], __locals: Dict, __globals: Dict):
    def get_valid_module(key: str, value: Any) -> Optional[Tuple[str, ModuleType]]:
        if not isinstance(value, Callable):
            return
        module = getmodule(value)
        if module not in modules.values():
            return
        return key, module

    locals_from_modules = dict(
        filter(None, starmap(get_valid_module, __locals.items()))
    )
    globals_from_modules = dict(
        filter(None, starmap(get_valid_module, __globals.items()))
    )
    local_modules = dict(
        (key, value)
        for key, value in __locals.items()
        if isinstance(value, ModuleType) and key != "__builtins__"
    )
    global_modules = dict(
        (key, value)
        for key, value in __globals.items()
        if isinstance(value, ModuleType) and key != "__builtins__"
    )
    local_as_translations = dict(
        (variable, get_module_variable(module, __locals, variable))
        for variable, module in locals_from_modules.items()
    )
    global_as_translations = dict(
        (variable, get_module_variable(module, __globals, variable))
        for variable, module in globals_from_modules.items()
    )
    dynamic_classes = dict(
        (module_name, get_dynamic_classes(module))
        for module_name, module in modules.items()
    )
    tuple(map(importlib.reload, modules.values()))
    local_modules = dict(
        (variable, re_import_dynamic_classes(module.__name__, dynamic_classes))
        for variable, module in local_modules.items()
    )
    global_modules = dict(
        (variable, re_import_dynamic_classes(module.__name__, dynamic_classes))
        for variable, module in global_modules.items()
    )
    locals_from_modules = dict(
        (
            variable,
            getattr(
                re_import_dynamic_classes(module.__name__, dynamic_classes),
                local_as_translations[variable],
            ),
        )
        for variable, module in locals_from_modules.items()
    )
    globals_from_modules = dict(
        (
            variable,
            getattr(
                re_import_dynamic_classes(module.__name__, dynamic_classes),
                global_as_translations[variable],
            ),
        )
        for variable, module in globals_from_modules.items()
    )
    for variable, value in locals_from_modules.items():
        __locals[variable] = value
    for variable, value in globals_from_modules.items():
        __globals[variable] = value
    for variable, module in local_modules.items():
        __locals[variable] = module
    for variable, module in global_modules.items():
        __globals[variable] = module
