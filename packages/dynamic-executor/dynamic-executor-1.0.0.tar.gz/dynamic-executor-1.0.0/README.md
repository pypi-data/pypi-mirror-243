# Dynamic-python library for changing python code during runtime

Dynamic python is ment to be used in test development for creating and updating tests or wherever the need arises to change the code during runtime and have results visible instantaneously without restarting. The main functionality is provided by `exec_in_dynamic_mode` generator that reloads all project-root modules (neither builtin not venv modules are reloaded)

## Installation

You can install the `dynamic-python` package using pip:

```bash
pip install dynamic-python
```

Or by cloning the repository directly :

```bash
git clone git@github.com:Tesla2000/dython.git
```

### Example

Here's an example of how to use the `exec_in_dynamic_mode` function:

```python
# ImportedModuleFaulty.py
from dython import DynamicClass


class SomeDynamicClass(DynamicClass):
    def foo(self):
        raise ValueError
```

```python
# ImportedModuleValid.py
from dython import DynamicClass


class SomeDynamicClass(DynamicClass):
    def foo(self):
        pass
```

```python
# test_executor.py
dynamic_instance.foo()
```

```python
from dython import exec_in_dynamic_mode
parent = Path(__file__).parent
parent.joinpath("ImportedModule.py").write_text(
    parent.joinpath("ImportedModuleFaulty.py").read_text()
)  # faulty version of imported module
from ImportedModule import SomeDynamicClass
dynamic_instance = SomeDynamicClass()
index = -1
for index, error in enumerate(exec_in_dynamic_mode(locals(), globals(), parent.joinpath("test_executor.py"))):
    if index:
        assert False  # ensuring that the error is corrected
    parent.joinpath("ImportedModule.py").write_text(
        parent.joinpath("ImportedModuleValid.py").read_text()
    )  # correcting module
```
