import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
boptions = {"bundle_name": "myApp"}

# GUI applications require a different base on Windows (the default is for a
# console application).

setup(name = "guifoo",
    version = "0.1",
    description ="My GUI application!",
    options = {"bdist_mac": boptions},
    executables = [Executable("execute.py")]
)
