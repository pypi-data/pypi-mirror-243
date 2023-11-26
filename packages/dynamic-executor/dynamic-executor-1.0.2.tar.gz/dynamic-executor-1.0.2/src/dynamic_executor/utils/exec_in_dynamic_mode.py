import traceback
from pathlib import Path
from typing import Generator

from src.dynamic_executor.utils import get_modules
from src.dynamic_executor.utils.re_import import re_import_modules


def exec_in_dynamic_mode(
    local_vars: dict,
    global_vars: dict,
    executor_path: Path = None,
    finnish_upon_success: bool = True,
) -> Generator[str, None, None]:
    if executor_path is None:
        executor_path = Path("executor.py")
    if not executor_path.exists():
        executor_path.write_text("# Save mode executor")
        yield f"Created an executor file in {executor_path.absolute()}"
    done = False
    while True:
        try:
            compiled = compile(executor_path.read_text(), executor_path.name, "exec")
            exec(compiled, global_vars, local_vars)
            done = True
        except:
            traceback.print_exc()
            yield traceback.format_exc()
        if not finnish_upon_success or not done:
            modules = get_modules()
            re_import_modules(modules, local_vars, global_vars)
        else:
            return
