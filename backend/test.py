from importlib import import_module
from glob import glob
from re import split

for module in glob('tests/*.py'):
    module = split(r'\/|\\',module[:-3])[1]
    if module=='__init__' or module.startswith("module_") or input(f"test {module} (y/n):") != 'y':
        continue
    import_module("tests."+module)