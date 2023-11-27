import re
import sys
import platform
from collections import OrderedDict

venv_module = (
    f"python{'.'.join(sys.version.split('.')[:2])}"
    if platform.system() == "Linux"
    else f"Python{''.join(sys.version.split('.')[:2])}"
)


def get_modules():
    return OrderedDict(
        (variable, value)
        for variable, value in sys.modules.items()
        if not re.findall(r"module \'[^\']+\' \((?:built-in|frozen)\)", str(value))
        and venv_module not in str(value)
        and not variable.startswith("_")
        and not any(
            map(
                variable.__contains__,
                (
                    "dynamic_executor",
                    "pyexpat",
                    "pydev",
                    "xml.parsers.expat.",
                    "typing.",
                    "cython_runtime",
                ),
            )
        )
    )
