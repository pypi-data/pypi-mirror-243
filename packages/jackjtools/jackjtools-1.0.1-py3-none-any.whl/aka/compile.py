import py_compile
import os
import shutil

class compile_():
    def __init__(self, path:str = ".") -> None:
        self.path = path

    def compile_to_pyc(self): 
        files = os.listdir(self.path)
        pyfiles = [x for x in files if x.endswith("py") and not x.startswith("__init__")]
        for f in pyfiles:
            py_compile.compile(f"{self.path}/{f}")
        shutil.copytree(f"{self.path}/__pycache__", "./jackjtools_")
        print(pyfiles)

