import traceback
from pathlib import Path
from typing import Generator, Dict

from .get_modules import get_modules
from .re_import import re_import_modules


class DynamicModeExecutor:
    def __init__(
        self,
        executor_path: Path = None,
        finnish_upon_success: bool = True,
        supress_print: bool = False,
    ):
        if executor_path is None:
            executor_path = Path("executor.py")
        self.executor_path = executor_path
        self.finnish_upon_success = finnish_upon_success
        self.supress_print = supress_print

    def execute(
        self,
        local_vars: Dict,
        global_vars: Dict,
        executor_path: Path = None,
        finnish_upon_success: bool = None,
        supress_print: bool = None,
    ) -> Generator[str, None, None]:
        if executor_path is None:
            executor_path = self.executor_path
        if supress_print is None:
            supress_print = self.supress_print
        if finnish_upon_success is None:
            finnish_upon_success = self.finnish_upon_success

        if not executor_path.exists():
            executor_path.write_text("# Save mode executor")
            yield f"Created an executor file in {executor_path.absolute()}"
        done = False
        while True:
            try:
                compiled = compile(
                    executor_path.read_text(), executor_path.name, "exec"
                )
                exec(compiled, global_vars, local_vars)
                done = True
            except:
                if not supress_print:
                    traceback.print_exc()
                yield traceback.format_exc()
            if not finnish_upon_success or not done:
                modules = get_modules()
                re_import_modules(modules, local_vars, global_vars)
            else:
                return
